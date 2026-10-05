#!/usr/bin/env bash
#
# Decide whether a merged preparation PR may publish an EDOT SDK release.
#
# Usage: publish-guard.sh
#
# Environment:
#   BASE_REF       target releasing branch of the merged PR (required)
#   HEAD_REF       source preparation branch of the merged PR (required)
#   MERGE_COMMIT   commit produced by merging the PR, 40 hexadecimal
#                  characters (required)
#   TAG_PREFIX     release tag prefix (`v` or empty)
#   VERSION_FILE   version file path, read by version-file.sh
#   VERSION_REGEX  version line regex, read by version-file.sh
#   GITHUB_OUTPUT  step output file (required)
#
# The consumer's publish workflow runs when a PR into a `releasing/*` branch
# is merged. GitHub's merge button already decided who may merge and whether
# the checks passed, so this script only confirms two things before anything
# irreversible happens:
#   - the merged commit is a prepared release: the version file at the merge
#     commit holds a release version X.Y.Z, the base branch is
#     `releasing/X.Y.Z`, and the merged head is `prepare/X.Y.Z`, so no other
#     PR into the releasing branch can publish;
#   - whether it was already published: the release tag is the lock. At the
#     merge commit, a previous run published and failed later, publication
#     is skipped, and only the remaining steps run. At another commit, a
#     different commit was released under this version and the run stops.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
base_ref=${BASE_REF:?BASE_REF is required}
head_ref=${HEAD_REF:?HEAD_REF is required}
release_sha=${MERGE_COMMIT:-}
output_file=${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}

# A short or symbolic value would make the checks below read a different
# commit than the one that was merged.
if [[ ! $release_sha =~ ^[0-9a-f]{40}$ ]]; then
  echo "merge-commit '$release_sha' is not a full commit SHA." >&2
  exit 1
fi

git fetch --quiet --tags origin "$release_sha"
version=$("$script_dir/../prepare-start/version-file.sh" read "$release_sha")
if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "The merged commit has version '$version', which is not a release version." >&2
  exit 1
fi
if [[ $base_ref != "releasing/$version" ]]; then
  echo "Expected base releasing/$version for version $version, found $base_ref." >&2
  exit 1
fi
if [[ $head_ref != "prepare/$version" ]]; then
  echo "Expected the merged head to be prepare/$version, found $head_ref." >&2
  exit 1
fi

# The tag is the record of what was published. Never move it.
tag="${TAG_PREFIX:-}$version"
tag_exists=false
if git rev-parse -q --verify "refs/tags/$tag^{commit}" >/dev/null; then
  tag_sha=$(git rev-parse "refs/tags/$tag^{commit}")
  if [[ $tag_sha != "$release_sha" ]]; then
    echo "Tag $tag exists at $tag_sha, not at the merged commit $release_sha." >&2
    exit 1
  fi
  echo "Tag $tag already exists at $release_sha; publication is skipped."
  tag_exists=true
fi

{
  echo "release-sha=$release_sha"
  echo "release-version=$version"
  echo "tag-exists=$tag_exists"
} >>"$output_file"
