#!/usr/bin/env bash
#
# Finish an EDOT SDK release after publish-guard accepted the merged
# preparation PR and the consumer's platform publication ran.
#
# Usage: finalize.sh
#
# Environment:
#   RELEASE_JSON        `release` output of publish-guard (required): the
#                       merged commit, the version, the release branch, and
#                       whether the tag already exists at the merged commit
#   DRY_RUN             true to print instead of create (default false)
#   RELEASE_REPOSITORY  owner/repository of the release (required). Not
#                       GITHUB_REPOSITORY: the runner owns the GITHUB_*
#                       variables.
#   GH_TOKEN            token with contents and pull-requests write access,
#                       used by every gh call (required)
#   GITHUB_SERVER_URL   GitHub base URL (default https://github.com)
#   GITHUB_OUTPUT       step output file (required)
#   RUNNER_TEMP         directory for work files (required)
#
# The platform facts come from the repository's EDOT release configuration
# (config.sh): tagPrefix, productName, docsUrl, headingAnchorPrefix, and
# versionFile and versionLine (via version-file.sh).
#
# In order: create the release tag at the merged commit; create the GitHub
# Release from the release-notes section; then finish by the patch digit. A
# zero patch digit commits the next `-SNAPSHOT` on `releasing/X.Y.Z` and
# opens that branch's PR into `main`. A nonzero patch digit is a patch
# release, which `main` never produces: it opens a notes-only PR into `main`.
# Last, it deletes `prepare/X.Y.Z`, and after a patch release also
# `releasing/X.Y.Z` and `patching/X.Y.Z`.
#
# Every step first checks whether its result already exists and skips it if
# so, so "Re-run failed jobs" picks up where a failed run stopped without
# repeating anything. Nothing is moved or republished. The guard owns the
# tag check; this script trusts its tagExists.
#
# With DRY_RUN=true the script runs every check and existence read, prints
# each command it would run with the Release and PR bodies, and creates
# nothing; `<release-url>` stands for the URL of a Release it did not create.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
release_json=${RELEASE_JSON:-}
dry_run=${DRY_RUN:-false}
repository=${RELEASE_REPOSITORY:?RELEASE_REPOSITORY is required}
: "${GH_TOKEN:?GH_TOKEN is required}"
output_file=${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}
work_dir=$(mktemp -d "${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-finalize.XXXXXX")
config_sh="$script_dir/../prepare-start/config.sh"
version_file_sh="$script_dir/../prepare-start/version-file.sh"
tag_prefix=$("$config_sh" get tagPrefix)
product_name=$("$config_sh" get productName)
docs_url=$("$config_sh" get docsUrl)
heading_anchor_prefix=$("$config_sh" get headingAnchorPrefix)
version_file=$("$config_sh" get versionFile)
notes_index=docs/release-notes/index.md

# Reject malformed values before anything is created; an empty or wrong
# value must never reach the tag or release commands.
if ! jq -e 'type == "object" and ([.sha, .version, .baseRef] | all(type == "string"))' \
  <<<"$release_json" >/dev/null 2>&1; then
  echo "release is not the JSON that publish-guard outputs." >&2
  exit 1
fi
release_sha=$(jq -r .sha <<<"$release_json")
release_version=$(jq -r .version <<<"$release_json")
base_ref=$(jq -r .baseRef <<<"$release_json")
tag_exists=$(jq -c .tagExists <<<"$release_json")
if [[ ! $release_sha =~ ^[0-9a-f]{40}$ ]]; then
  echo "sha '$release_sha' is not a full commit SHA." >&2
  exit 1
fi
if [[ ! $release_version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "version '$release_version' is not X.Y.Z." >&2
  exit 1
fi
# A JSON boolean only; jq -c prints a string with its quotes.
if [[ $tag_exists != true && $tag_exists != false ]]; then
  echo "tagExists $tag_exists must be true or false." >&2
  exit 1
fi
if [[ $dry_run != true && $dry_run != false ]]; then
  echo "dry-run '$dry_run' must be true or false." >&2
  exit 1
fi
if [[ $base_ref != "releasing/$release_version" ]]; then
  echo "Unexpected release branch $base_ref for version $release_version." >&2
  exit 1
fi

tag="$tag_prefix$release_version"
tag_url="${GITHUB_SERVER_URL:-https://github.com}/$repository/releases/tag/$tag"

# Every command that creates a ref, a commit, a push, a Release, or a PR
# goes through run, so the dry-run prints exactly what a real run executes.
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

# Explicit refspecs keep the remote-tracking refs current whatever the
# checkout's fetch configuration is.
git fetch --quiet --tags origin \
  "refs/heads/main:refs/remotes/origin/main" \
  "refs/heads/$base_ref:refs/remotes/origin/$base_ref"

# Print the URL of an open or merged PR from <head-ref> into main, or nothing.
# A failed lookup must not read as "no PR": the function runs in a command
# substitution, where set -e does not apply, so it returns the failure and
# the caller's assignment stops the script.
find_main_pr() {
  local head_ref=$1
  local found=
  local state
  for state in open merged; do
    found=$(
      gh pr list \
        --repo "$repository" \
        --state "$state" \
        --base main \
        --head "$head_ref" \
        --limit 1 \
        --json url \
        --jq '.[0].url // empty'
    ) || {
      echo "Could not list $state pull requests from $head_ref into main in $repository." >&2
      return 1
    }
    [[ -z $found ]] || break
  done
  printf '%s\n' "$found"
}

# Extract the released section once, before anything irreversible. It is
# shared by the GitHub Release and the patch notes-only PR. The heading is
# matched literally, so the dots of the version match only dots.
release_section="$work_dir/release-section.md"
git show "$release_sha:$notes_index" \
  | awk -v heading="## $release_version " '
      index($0, heading) == 1 { capture = 1; print; next }
      capture && /^## / { exit }
      capture { print }
    ' >"$release_section"
if [[ ! -s $release_section ]]; then
  echo "Could not extract release notes for $release_version from $notes_index at $release_sha." >&2
  exit 1
fi

# Publication for a repository whose consumers resolve the tag. The guard
# already validated an existing tag; create it only when absent. A tag is
# never moved.
if [[ $tag_exists == false ]]; then
  run git tag "$tag" "$release_sha"
  run git push origin "refs/tags/$tag:refs/tags/$tag"
fi

# The GitHub Release body is the section plus the published-docs link.
# --verify-tag makes gh fail instead of creating a missing tag itself.
if gh release view "$tag" --repo "$repository" >/dev/null 2>&1; then
  echo "GitHub Release $tag already exists."
  release_url=$(gh release view "$tag" --repo "$repository" --json url --jq .url)
else
  release_body="$work_dir/github-release.md"
  cp "$release_section" "$release_body"
  printf '\n[Published documentation](%s#%s%s-release-notes)\n' \
    "$docs_url" "$heading_anchor_prefix" "${release_version//./}" >>"$release_body"
  release_url=$(
    run gh release create "$tag" \
      --repo "$repository" \
      --verify-tag \
      --title "$product_name $release_version" \
      --notes-file "$release_body"
  )
  if [[ $dry_run == true ]]; then
    echo 'Release body:'
    cat "$release_body"
    release_url='<release-url>'
  fi
fi

body_file="$work_dir/main-pull-request-body.md"
if [[ ${release_version##*.} == 0 ]]; then
  # Move the release branch to the next development version. The tag stays
  # on the merged commit; this commit comes right after it. Commit only while
  # the branch still points at the merged commit. A single commit on top that
  # only sets the next development version is this step from a previous run.
  # Anything else means the branch moved, and opening the release PR would
  # bring unpublished changes into main.
  next_development=$("$script_dir/../version/version.sh" next-development "$release_version")
  branch_tip=$(git rev-parse "refs/remotes/origin/$base_ref")
  if [[ $branch_tip == "$release_sha" ]]; then
    run git switch -C "$base_ref" "$release_sha"
    run "$version_file_sh" write "$next_development"
    run git add -- "$version_file"
    run git commit -m "Prepare for the next release"
    run git push origin "HEAD:refs/heads/$base_ref"
  elif [[ $(git rev-parse "$branch_tip^") == "$release_sha" \
    && $(git diff --name-only "$release_sha" "$branch_tip") == "$version_file" \
    && $("$version_file_sh" read "$branch_tip") == "$next_development" ]]; then
    echo "$base_ref already carries the next development version."
  else
    echo "$base_ref moved after the merge: its tip is $branch_tip, expected $release_sha or its bump commit. Not opening a release PR from unpublished changes." >&2
    exit 1
  fi

  main_pr=$(find_main_pr "$base_ref")
  if [[ -n $main_pr ]]; then
    echo "Release PR into main already exists: $main_pr"
  else
    # The backticks below are Markdown, not command substitution.
    # shellcheck disable=SC2016
    {
      printf '%s %s is published: [%s](%s), [GitHub Release](%s).\n\n' \
        "$product_name" "$release_version" "$tag" "$tag_url" "$release_url"
      printf 'This pull request brings the release changes into `main` and sets the development version to `%s`. Merge it to finish the release.\n' \
        "$next_development"
    } >"$body_file"
    # The operator merges this PR to bring the release and the next
    # development version into main; the automation never merges it.
    main_pr=$(
      run gh pr create \
        --repo "$repository" \
        --base main \
        --head "$base_ref" \
        --title "Release $release_version" \
        --body-file "$body_file"
    )
  fi
else
  # The notes-only PR into main. A previous run may have pushed the notes
  # branch and failed before opening the PR: open the PR from that branch.
  # Otherwise build it from main, inserting the section above the first
  # heading with a lower version; the index is in descending order, so that
  # is its place.
  notes_branch="patch-notes/$release_version"
  main_pr=$(find_main_pr "$notes_branch")
  if [[ -n $main_pr ]]; then
    echo "Release notes PR into main already exists: $main_pr"
  else
    if git ls-remote --exit-code --heads origin "refs/heads/$notes_branch" >/dev/null 2>&1; then
      echo "$notes_branch already exists; opening its pull request."
    else
      if git show "refs/remotes/origin/main:$notes_index" | grep -Eq "^## ${release_version//./\\.} "; then
        echo "Release notes for $release_version are already on main, but no open or merged $notes_branch pull request was found." >&2
        exit 1
      fi
      updated_index="$work_dir/index.md"
      if ! git show "refs/remotes/origin/main:$notes_index" \
        | awk -v version="$release_version" -v notes="$release_section" '
          function lower(a, b,    x, y, i) {
            split(a, x, "."); split(b, y, ".")
            for (i = 1; i <= 3; i++) if (x[i] != y[i]) return x[i] + 0 < y[i] + 0
            return 0
          }
          !inserted && /^## [0-9]+\.[0-9]+\.[0-9]+ / && lower($2, version) {
            while ((getline entry < notes) > 0) print entry
            close(notes)
            inserted = 1
          }
          { print }
          END { exit !inserted }
        ' >"$updated_index"; then
        echo "main has no release-notes section older than $release_version; cannot place its notes." >&2
        exit 1
      fi
      run git switch -C "$notes_branch" refs/remotes/origin/main
      run cp "$updated_index" "$notes_index"
      run git add -- "$notes_index"
      run git commit -m "Add $release_version release notes"
      run git push origin "HEAD:refs/heads/$notes_branch"
    fi

    {
      printf '%s %s is published: [%s](%s), [GitHub Release](%s).\n\n' \
        "$product_name" "$release_version" "$tag" "$tag_url" "$release_url"
      printf 'Merging this pull request publishes the release notes on the documentation site.\n'
    } >"$body_file"
    # The docs site deploys from main, so the patch's notes appear only once
    # the operator merges this PR.
    main_pr=$(
      run gh pr create \
        --repo "$repository" \
        --base main \
        --head "$notes_branch" \
        --title "Release notes for $release_version" \
        --body-file "$body_file"
    )
  fi
fi

# Delete the branches the release no longer needs; the tag keeps the
# released commit. This runs last: until here, a rerun of the publish job
# needs releasing/X.Y.Z, which publish-guard checks. On main, releasing/X.Y.Z
# is the head of the PR into main and stays. A branch that is already gone
# is skipped; a failed lookup stops the script.
finished_branches=("prepare/$release_version")
if [[ ${release_version##*.} != 0 ]]; then
  finished_branches+=("$base_ref" "patching/$release_version")
fi
for branch in "${finished_branches[@]}"; do
  remote_head=$(git ls-remote --heads origin "refs/heads/$branch")
  if [[ -n $remote_head ]]; then
    run git push origin --delete "$branch"
  else
    echo "$branch is already deleted."
  fi
done

if [[ $dry_run == true ]]; then
  if [[ -s $body_file ]]; then
    echo 'Pull request body:'
    cat "$body_file"
  fi
  release_url=
  main_pr=
else
  echo "GitHub Release: $release_url"
  echo "Pull request into main: $main_pr"
fi
{
  echo "release-url=$release_url"
  echo "main-pull-request-url=$main_pr"
} >>"$output_file"
