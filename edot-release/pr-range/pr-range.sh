#!/usr/bin/env bash
#
# List the pull requests that go into the next release.
#
# Usage: pr-range.sh [ref] [previous-tag]
#
# Arguments:
#   ref           commit or ref at the end of the range (default HEAD)
#   previous-tag  release tag at the start of the range (default the highest
#                 tag per ../version/version.sh, honoring TAG_PREFIX)
#
# Environment:
#   RELEASE_REPOSITORY  owner/repository to query (default the current gh
#                       repository). Not GITHUB_REPOSITORY: the runner owns
#                       the GITHUB_* variables and ignores an override, so a
#                       consumer could never point the action elsewhere.
#   GH_TOKEN            GitHub CLI authentication in CI; local gh
#                       authentication is used when unset
#   TAG_PREFIX          release tag prefix, read by version.sh
#
# Walks the first-parent commits between `git merge-base <previous-tag> <ref>`
# and <ref> and resolves each one to its merged pull request through GitHub's
# "pull requests associated with a commit" endpoint. The range starts at the
# merge base because release tags are not ancestors of `main`: the release
# commit lives on its own releasing branch. `main` is squash-merged, so each
# first-parent commit is one PR. A commit with no PR resolves through the
# full-SHA `(cherry picked from commit <sha>)` trailer that a bot cherry-pick
# carries; otherwise the script stops, because the release notes could not
# account for it. PRs from `releasing/*`, `prepare/*`, and `patch-notes/*`
# heads are release bookkeeping and are left out. Prints JSON with the tag,
# the range, and one entry per PR (number, title, URL, labels).

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ref=${1:-HEAD}
previous_tag=${2:-}
repository=${RELEASE_REPOSITORY:-}

if [[ -z $repository ]]; then
  repository=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
fi
if [[ -z $previous_tag ]]; then
  previous_tag=$("$script_dir/../version/version.sh" highest-tag)
fi
if ! git rev-parse --verify "$previous_tag^{commit}" >/dev/null 2>&1; then
  echo "Previous tag '$previous_tag' does not resolve to a commit." >&2
  exit 1
fi
if ! head_sha=$(git rev-parse --verify "$ref^{commit}" 2>/dev/null); then
  echo "Ref '$ref' does not resolve to a commit." >&2
  exit 1
fi

base_sha=$(git merge-base "$previous_tag" "$head_sha")
pull_requests='[]'

# Prefer the PR whose merge commit is this exact commit. Fall back to the
# single merged PR in this repository when the API lists only one. A commit
# GitHub does not know (404) counts as "no PR", so the trailer fallback and
# the stop message below apply; any other API failure stops the run with the
# API's message.
resolve_pull_request() {
  local commit=$1
  local associated
  if ! associated=$(
    gh api \
      -H "Accept: application/vnd.github+json" \
      "repos/$repository/commits/$commit/pulls?per_page=100" 2>&1
  ); then
    if [[ $associated == *"No commit found for SHA"* ]]; then
      return 0
    fi
    echo "GitHub API request failed for commit $commit: $associated" >&2
    exit 1
  fi
  jq -c \
    --arg repository "$repository" \
    --arg commit "$commit" \
    '[
       .[]
       | select(
           .merged_at != null
           and .base.repo.full_name == $repository
           and .merge_commit_sha == $commit
         )
     ] as $exact
     | if ($exact | length) == 1 then
         $exact[0]
       else
         [.[] | select(.merged_at != null and .base.repo.full_name == $repository)] as $eligible
         | if ($eligible | length) == 1 then $eligible[0] else empty end
       end' <<<"$associated"
}

while IFS= read -r commit_sha; do
  [[ -n $commit_sha ]] || continue
  pull_request=$(resolve_pull_request "$commit_sha")
  if [[ -z $pull_request ]]; then
    # A bot cherry-pick has no PR of its own; its `-x` trailer names the
    # commit on main that does.
    commit_message=$(git show -s --format=%B "$commit_sha")
    if [[ $commit_message =~ \(cherry\ picked\ from\ commit\ ([0-9a-fA-F]{40})\) ]]; then
      pull_request=$(resolve_pull_request "${BASH_REMATCH[1]}")
    fi
  fi
  if [[ -z $pull_request ]]; then
    echo "Commit $commit_sha has no associated merged pull request in $repository." >&2
    exit 1
  fi

  # Release bookkeeping PRs (the preparation PR, the release PR into main,
  # the patch notes PR) describe a release rather than contribute to one.
  head_ref=$(jq -r '.head.ref' <<<"$pull_request")
  if [[ $head_ref == releasing/* || $head_ref == prepare/* || $head_ref == patch-notes/* ]]; then
    continue
  fi

  item=$(
    jq -c \
      '{
        number: .number,
        title: .title,
        url: .html_url,
        labels: [.labels[].name]
      }' <<<"$pull_request"
  )
  pull_requests=$(jq -c --argjson item "$item" '. + [$item]' <<<"$pull_requests")
done < <(git rev-list --first-parent --reverse "$base_sha..$head_sha")

jq -n \
  --arg previous_tag "$previous_tag" \
  --arg base_sha "$base_sha" \
  --arg head_sha "$head_sha" \
  --argjson pull_requests "$pull_requests" \
  '{
    previousTag: $previous_tag,
    baseSha: $base_sha,
    headSha: $head_sha,
    pullRequests: $pull_requests
  }'
