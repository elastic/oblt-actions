#!/usr/bin/env bash
#
# Finish preparing an EDOT SDK release: push the release branches and open
# the preparation PR.
#
# Usage: prepare-finish.sh
#
# Environment:
#   RELEASE_VERSION     release version, X.Y.Z (required)
#   RELEASE_BUMP        bump derived by prepare-start: minor or major
#   PREVIOUS_TAG        tag of the previous release (required)
#   RELEASE_RANGE       range JSON from prepare-start (required)
#   RELEASE_REF         dispatched commit (required)
#   RELEASE_PATHS       pathspecs to stage, one per line (required)
#   PRODUCT_NAME        product name in the PR body, such as EDOT iOS
#   TAG_PREFIX          release tag prefix (`v` or empty)
#   DRY_RUN             true to print instead of create (default false)
#   RELEASE_REPOSITORY  owner/repository where the PR is opened (required).
#                       Not GITHUB_REPOSITORY: the runner owns the GITHUB_*
#                       variables.
#   GH_TOKEN            GitHub CLI authentication; a token that triggers
#                       workflows, so ordinary CI runs on the PR
#   GITHUB_OUTPUT       step output file (required)
#   RUNNER_TEMP         directory for work files (required)
#
# Runs after prepare-start and the consumer's platform steps have written
# the release changes into the working tree. Pushes `releasing/X.Y.Z` at the
# dispatched commit, unchanged, then commits the release changes once on
# `prepare/X.Y.Z` and opens the preparation PR between them, so the PR diff
# shows exactly what the release adds. Merging that PR publishes the
# release; nothing here is irreversible on its own, but the pushed branches
# are the in-flight lock that blocks the next preparation.
#
# With DRY_RUN=true the script runs every check, prints each command it
# would run, the paths it would stage, and the PR body, and creates nothing.

set -euo pipefail

release_version=${RELEASE_VERSION:-}
bump=${RELEASE_BUMP:-}
previous_tag=${PREVIOUS_TAG:?PREVIOUS_TAG is required}
release_range=${RELEASE_RANGE:?RELEASE_RANGE is required}
release_ref=${RELEASE_REF:?RELEASE_REF is required}
product_name=${PRODUCT_NAME:?PRODUCT_NAME is required}
repository=${RELEASE_REPOSITORY:?RELEASE_REPOSITORY is required}
output_file=${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}
work_dir=$(mktemp -d "${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-prepare-finish.XXXXXX")
dry_run=${DRY_RUN:-false}

# Reject malformed values before anything is pushed.
if [[ ! $release_version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "version '$release_version' is not X.Y.Z." >&2
  exit 1
fi
if [[ $bump != minor && $bump != major ]]; then
  echo "bump '$bump' must be minor or major." >&2
  exit 1
fi
if [[ $dry_run != true && $dry_run != false ]]; then
  echo "dry-run '$dry_run' must be true or false." >&2
  exit 1
fi
if ! jq -e '.pullRequests | type == "array"' <<<"$release_range" >/dev/null 2>&1; then
  echo "range is not the JSON that prepare-start outputs." >&2
  exit 1
fi
# One pathspec per line; blank lines are ignored. Pathspec magic such as
# `:(glob)**/generated.txt` passes through to git unchanged.
paths=()
while IFS= read -r path; do
  if [[ -n $path ]]; then
    paths+=("$path")
  fi
done <<<"${RELEASE_PATHS:-}"
if [[ ${#paths[@]} -eq 0 ]]; then
  echo "paths must list at least one pathspec." >&2
  exit 1
fi

# Every command that changes a ref, the index, or GitHub goes through run, so
# the dry-run prints exactly what a real run executes. The printout goes to
# file descriptor 3, the original standard output, so it stays visible when
# a caller captures a command's output.
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

release_branch="releasing/$release_version"
prepare_branch="prepare/$release_version"
tag="${TAG_PREFIX:-}$release_version"

body_file="$work_dir/pull-request-body.md"
# `main` never produces a patch, so a nonzero patch digit means a patch
# release, whose finalize opens a notes-only PR instead of the release PR.
if [[ ${release_version##*.} == 0 ]]; then
  ending="a pull request from \`$release_branch\` into \`main\`"
else
  ending="a release-notes pull request into \`main\`"
fi
# The backticks below are Markdown, not command substitution.
# shellcheck disable=SC2016
{
  printf 'Prepare %s %s.\n\n' "$product_name" "$release_version"
  printf -- '- Bump: `%s`\n' "$bump"
  printf -- '- Previous release: `%s`\n' "$previous_tag"
  printf -- '- Included pull requests:\n'
  jq -r '.pullRequests[] | "- [#\(.number)](\(.url)) \(.title)"' <<<"$release_range"
  printf '\n> Merging this pull request publishes %s: the automation tags the merge commit as `%s`, creates the GitHub Release, and opens %s. Review it, then merge when the checks are green.\n' \
    "$release_version" "$tag" "$ending"
} >"$body_file"

# The release branch is the dispatched commit, untouched; it is the base of
# the preparation PR and later of the release PR into main.
run git branch "$release_branch" "$release_ref"
run git push origin "refs/heads/$release_branch:refs/heads/$release_branch"
# The release changes sit uncommitted in the working tree; the prepare branch
# starts at the same commit and takes them along.
run git switch -c "$prepare_branch"
# Stage additions too: a platform step can create files the release must
# ship. Only the listed paths are staged.
if [[ $dry_run == true ]]; then
  echo 'Paths that would be staged:'
  git add --dry-run -A -- "${paths[@]}"
fi
run git add -A -- "${paths[@]}"
run git commit -m "Prepare release $release_version"
run git push origin "HEAD:refs/heads/$prepare_branch"

# Merging this PR is the operator's release action; it is not a draft. The
# automation never writes to it again after opening it.
pr_url=$(
  run gh pr create \
    --repo "$repository" \
    --base "$release_branch" \
    --head "$prepare_branch" \
    --title "Prepare release $release_version" \
    --body-file "$body_file"
)
if [[ $dry_run == true ]]; then
  echo 'Pull request body:'
  cat "$body_file"
  pr_url=
else
  echo "Preparation pull request: $pr_url"
fi
echo "pull-request-url=$pr_url" >>"$output_file"
