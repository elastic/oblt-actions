#!/usr/bin/env bash
#
# Start an EDOT SDK patch release: cut `patching/X.Y.Z` from the highest
# release tag of a line and cherry-pick merged `main` pull requests onto it.
#
# Usage: start-patch.sh
#
# Environment:
#   LINE                release line to patch, X.Y (required)
#   PULL_REQUESTS       `main` pull requests to cherry-pick, numbers separated
#                       by commas, such as 1135,527
#   RELEASE_REF_NAME    dispatched branch; must be `main`
#   DRY_RUN             true to print the push instead of running it
#                       (default false)
#   RELEASE_REPOSITORY  owner/repository of the pull requests (required),
#                       under its own name because the runner owns the
#                       GITHUB_* variables
#   GH_TOKEN            token with pull-requests read access, used by the
#                       pull request lookups
#   RUNNER_TEMP         directory for work files (required)
#
# The tag prefix comes from the repository's EDOT release configuration
# (config.sh). The checkout needs full history and tags and a Git identity.
#
# Only a tag that contains `.github/edot-release.json` can be patched. A
# patch branch runs the release workflows of its source tag, and that file
# arrived together with the shared release actions, which handle patch
# branches. An older release is patched by hand.
#
# In order: check the inputs, resolve the source tag and the next patch
# version, stop if the patch branch exists, look up every pull request, then
# cherry-pick them with -x in merge order on a detached HEAD at the tag. Only
# after every check and cherry-pick succeeded does it push, once. A failure
# pushes nothing, and on every exit the original checkout is restored.
#
# With DRY_RUN=true every check, lookup, and cherry-pick runs, and the push is
# printed instead of run. The picked commits stay only as unreferenced
# objects.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
line=${LINE:-}
pull_requests=${PULL_REQUESTS:-}
ref_name=${RELEASE_REF_NAME:-}
dry_run=${DRY_RUN:-false}
repository=${RELEASE_REPOSITORY:?RELEASE_REPOSITORY is required}
work_dir=$(mktemp -d "${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-start-patch.XXXXXX")
version_sh="$script_dir/../version/version.sh"
config_sh="$script_dir/../prepare-start/config.sh"

if [[ $dry_run != true && $dry_run != false ]]; then
  echo "dry-run '$dry_run' must be true or false." >&2
  exit 1
fi
# Start patch is dispatched from main only. The patch branch starts from a
# tag, never from the dispatched branch.
if [[ $ref_name != main ]]; then
  echo "Start patch runs from main, not '$ref_name'." >&2
  exit 1
fi
# version.sh would read an empty line as "every line" and pick the highest
# tag of the repository.
if [[ -z $line ]]; then
  echo "line is required; expected X.Y." >&2
  exit 1
fi

# version.sh reads the tag prefix from the environment.
TAG_PREFIX=$("$config_sh" get tagPrefix)
export TAG_PREFIX
source_tag=$("$version_sh" highest-tag "$line")

if ! git cat-file -e "$source_tag:.github/edot-release.json" 2>/dev/null; then
  echo "$source_tag predates the automated release process; patch this release by hand." >&2
  exit 1
fi

release_version=$("$version_sh" next-patch "$source_tag")
patch_branch="patching/$release_version"
# Exit 2 means no such branch. A failed read never counts as absent.
ls_remote_status=0
git ls-remote --exit-code --heads origin "refs/heads/$patch_branch" >/dev/null || ls_remote_status=$?
case $ls_remote_status in
  0)
    echo "$patch_branch already exists; cherry-pick further fixes by hand through pull requests into that branch." >&2
    exit 1
    ;;
  2) ;;
  *)
    echo "Could not list origin's branches." >&2
    exit 1
    ;;
esac

if [[ -n $pull_requests && ! $pull_requests =~ ^[1-9][0-9]*(,[1-9][0-9]*)*$ ]]; then
  echo "Invalid pull-requests '$pull_requests'; expected numbers separated by commas, such as 1135,527." >&2
  exit 1
fi
requested_file="$work_dir/pull-requests.tsv"
: >"$requested_file"
IFS=, read -r -a numbers <<<"$pull_requests"
for number in ${numbers[@]+"${numbers[@]}"}; do
  pr=$(
    gh pr view "$number" \
      --repo "$repository" \
      --json number,state,baseRefName,mergedAt,mergeCommit
  )
  if ! jq -e '.state == "MERGED" and .baseRefName == "main"' <<<"$pr" >/dev/null; then
    echo "Pull request #$number must be merged into main in $repository." >&2
    exit 1
  fi
  merge_commit=$(jq -r .mergeCommit.oid <<<"$pr")
  # Cherry-picking a merge commit needs a mainline choice, and picking a
  # squash commit is what makes one PR one commit on the patch branch. A
  # rebase merge leaves a one-parent commit and is not detected here.
  parents=$(git show -s --format=%P "$merge_commit")
  if [[ $parents == *' '* ]]; then
    echo "Pull request #$number was not squash-merged: its merge commit $merge_commit has more than one parent. Dispatch again without #$number, then cherry-pick it by hand through a pull request into $patch_branch. Nothing was pushed." >&2
    exit 1
  fi
  jq -r '[.mergedAt, (.number | tostring), .mergeCommit.oid] | @tsv' <<<"$pr" >>"$requested_file"
done
# ISO 8601 timestamps sort in time order as plain strings.
LC_ALL=C sort -o "$requested_file" "$requested_file"

# Put the checkout back as it was found, the branch or the detached commit,
# on every exit: a failed cherry-pick is aborted first, a failure must not
# leave a half-built patch checked out, and a dry-run must leave nothing
# behind but unreferenced objects.
original_branch=$(git symbolic-ref -q --short HEAD || true)
original_commit=$(git rev-parse HEAD)
restore_checkout() {
  if git rev-parse -q --verify CHERRY_PICK_HEAD >/dev/null; then
    git cherry-pick --abort
  fi
  if [[ -n $original_branch ]]; then
    git switch --quiet "$original_branch"
  else
    git switch --quiet --detach "$original_commit"
  fi
}
trap restore_checkout EXIT

# Pick on a detached HEAD at the tag in both modes, so the action never
# creates a local branch; the push below names the remote branch directly.
git switch --quiet --detach "$source_tag"
while IFS=$'\t' read -r _merged_at number merge_commit; do
  # -x records the original commit, which pr-range uses to resolve the
  # pull request of each patch commit.
  if ! git cherry-pick -x "$merge_commit"; then
    # The EXIT trap aborts the cherry-pick and restores the checkout.
    echo "Cherry-pick for pull request #$number conflicted. Dispatch again without #$number, then cherry-pick it by hand through a pull request into $patch_branch. Nothing was pushed." >&2
    exit 1
  fi
done <"$requested_file"
patch_commit=$(git rev-parse HEAD)

# The printout goes to file descriptor 3, the original standard output, so
# it stays visible when a caller captures a command's output.
exec 3>&1
run() {
  if [[ $dry_run == true ]]; then
    printf 'Would run:' >&3
    printf ' %q' "$@" >&3
    printf '\n' >&3
  else
    "$@"
  fi
}

# Every check and cherry-pick succeeded. This is the only write to origin,
# and it creates the patch branch at the last picked commit. The empty lease
# makes the push fail if the branch appeared after the check above, such as
# from a concurrent run, instead of advancing that branch.
run git push --force-with-lease="refs/heads/$patch_branch:" origin "$patch_commit:refs/heads/$patch_branch"
