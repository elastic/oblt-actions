#!/usr/bin/env bash
#
# Start preparing an EDOT SDK release: check the dispatch, derive the
# release, and write the release changes into the working tree.
#
# Usage: prepare-start.sh
#
# Environment:
#   RELEASE_NOTES             release-note JSON authored by the operator
#   RELEASE_REF               dispatched commit (required)
#   RELEASE_REF_NAME          dispatched branch name: main or patching/X.Y.Z
#   RELEASE_REPOSITORY        owner/repository whose pull requests are listed
#                             and linked (required). Not GITHUB_REPOSITORY:
#                             the runner owns the GITHUB_* variables.
#   GH_TOKEN                  GitHub CLI authentication, read by pr-range.sh
#   GITHUB_OUTPUT             step output file (required)
#   RUNNER_TEMP               directory for work files (required)
#
# The platform facts come from the repository's EDOT release configuration
# (config.sh): tagPrefix, versionFile and versionLine (via version-file.sh),
# headingAnchorPrefix, subsectionAnchorPrefix, and appliesToKey.
#
# On main, the bump comes from the notes (`major` when any item is breaking,
# else `minor`) and the version from the previous tag, after checking that
# the version file holds the expected `-SNAPSHOT`. On a patch branch, the
# bump is `patch`, the version comes from the branch name `patching/X.Y.Z`,
# and the branch must contain its source tag. Then the script sets the
# version file, rewrites `applies_to` entries that name a development version
# that will never ship, and inserts the rendered section under the
# `% next_release_notes` marker.
#
# Every check runs before the first file is written, and the script creates
# no ref, commit, or push: platform steps such as NOTICE regeneration run in
# the consumer workflow next, and the prepare-finish action then pushes and
# opens the preparation PR. Outputs `prepared`, `version`, `previous-tag`,
# and `release`, the JSON prepare-finish takes: version, bump, previousTag,
# releaseBranch, prepareBranch, and range. If no PR was merged since the
# previous release, the script succeeds with `prepared=false`, sets only
# `previous-tag`, and writes nothing.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
release_notes=${RELEASE_NOTES:-}
release_ref=${RELEASE_REF:?RELEASE_REF is required}
release_ref_name=${RELEASE_REF_NAME:-}
: "${RELEASE_REPOSITORY:?RELEASE_REPOSITORY is required}"
output_file=${GITHUB_OUTPUT:?GITHUB_OUTPUT is required}
work_dir=$(mktemp -d "${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-prepare-start.XXXXXX")
config_sh="$script_dir/config.sh"
tag_prefix=$("$config_sh" get tagPrefix)
heading_anchor_prefix=$("$config_sh" get headingAnchorPrefix)
subsection_anchor_prefix=$("$config_sh" get subsectionAnchorPrefix)
applies_to_key=$("$config_sh" get appliesToKey)
# version.sh and pr-range.sh read the tag prefix from the environment.
export TAG_PREFIX=$tag_prefix
version_sh="$script_dir/../version/version.sh"
version_file_sh="$script_dir/version-file.sh"
notes_index=docs/release-notes/index.md
marker='% next_release_notes'

# `main` releases the next minor or major; `patching/X.Y.Z` releases X.Y.Z.
# Any other branch has no defined release, so stop before reading its state.
if [[ $release_ref_name != main && $release_ref_name != patching/* ]]; then
  echo "Prepare release runs from main or a patching/X.Y.Z branch, not '$release_ref_name'." >&2
  exit 1
fi

# Only one release can be in flight. A releasing branch exists from the
# moment preparation pushes it until the release is finished and the branch
# deleted. This read is not a lock: it assumes the caller runs every
# preparation, main and patch, in one concurrency group without
# cancel-in-progress, so no second run starts until the first has pushed.
existing_release_branches=$(git ls-remote --heads origin 'refs/heads/releasing/*' | awk '{print $2}')
if [[ -n $existing_release_branches ]]; then
  echo "A release is already in flight. Finish it, or delete its branches if it was abandoned:" >&2
  printf '%s\n' "${existing_release_branches//refs\/heads\//  }" >&2
  exit 1
fi

previous_tag=$("$version_sh" previous-tag "$release_ref_name")
patch_release=false
if [[ $release_ref_name == patching/* ]]; then
  patch_release=true
  release_version=${release_ref_name#patching/}
  if ! git merge-base --is-ancestor "$previous_tag" "$release_ref" 2>/dev/null; then
    echo "$release_ref_name must contain its source tag $previous_tag." >&2
    exit 1
  fi
  # A leftover branch of a shipped patch would otherwise pass here and stop
  # only at the publish guard, after its preparation PR was merged.
  if git rev-parse -q --verify "refs/tags/$tag_prefix$release_version" >/dev/null; then
    echo "$tag_prefix$release_version is already released; delete $release_ref_name instead of preparing it again." >&2
    exit 1
  fi
fi

range_file="$work_dir/range.json"
"$script_dir/../pr-range/pr-range.sh" "$release_ref" "$previous_tag" >"$range_file"

# Nothing to release is a successful outcome, not an error, whatever the
# notes say: the consumer workflow skips the remaining phases.
if [[ $(jq '.pullRequests | length' "$range_file") -eq 0 ]]; then
  echo "No contributing pull requests since $previous_tag remain after excluding release bookkeeping; preparation is a no-op."
  {
    echo 'prepared=false'
    echo "previous-tag=$previous_tag"
  } >>"$output_file"
  exit 0
fi

notes_file="$work_dir/release-notes.json"
if [[ -z $release_notes ]] || ! jq . <<<"$release_notes" >"$notes_file" 2>/dev/null; then
  echo "The release_notes input is not valid JSON." >&2
  exit 1
fi
# The breaking flag is the only bump signal; render-release-notes.sh below
# validates the shape and rejects a text-only `[Breaking]` prefix.
bump=$(
  jq -r \
    '[.dependencies[]?, .featuresEnhancements[]?, .fixes[]?, .uncategorized[]?]
     | if any(.breaking? == true) then "major" else "minor" end' \
    "$notes_file"
)
if [[ $patch_release == true && $bump == major ]]; then
  echo "A patch release cannot contain a breaking item." >&2
  exit 1
fi
if [[ $patch_release == true ]]; then
  bump="patch"
else
  development_version=$("$version_file_sh" read)
  release_version=$(
    "$version_sh" release-version "$previous_tag" "$development_version" "$bump"
  )
fi
release_branch="releasing/$release_version"
prepare_branch="prepare/$release_version"

# The anchor bases carry the version digits, for example
# `elastic-apm-android-agent-1100` for 1.10.0.
version_digits=${release_version//./}
section_file="$work_dir/release-notes.md"
"$script_dir/../render-release-notes/render-release-notes.sh" \
  "$notes_file" \
  "$release_version" \
  "$heading_anchor_prefix$version_digits" \
  "$subsection_anchor_prefix$version_digits" \
  >"$section_file"

if [[ $(grep -Fxc "$marker" "$notes_index") -ne 1 ]]; then
  echo "Expected exactly one '$marker' line in $notes_index." >&2
  exit 1
fi
# The dots are escaped so that 1.10.0 cannot match a 1x10x0 heading.
if grep -Eq "^## ${release_version//./\\.} " "$notes_index"; then
  echo "Release notes for $release_version already exist in $notes_index." >&2
  exit 1
fi

# Every check passed. From here on the script writes the working tree.
"$version_file_sh" write "$release_version"

# Documentation `applies_to` entries name the version a change ships in. They
# were written against the development version; on a major bump that version
# is never released, so rewrite them to the release version. The match stays
# on one line, and the lookahead keeps 1.1.0 from matching inside 1.1.0.1 or
# 1.1.01. A patch release never rewrites them: its branch holds released
# documentation.
if [[ $patch_release == false && $release_version != "${development_version%-SNAPSHOT}" ]]; then
  while IFS= read -r -d '' file; do
    APPLIES_TO_KEY=$applies_to_key OLD_VERSION=${development_version%-SNAPSHOT} NEW_VERSION=$release_version \
      perl -pi -e '
        s/(\Q$ENV{APPLIES_TO_KEY}\E:[ \t]+[a-z_]+[ \t]+)\Q$ENV{OLD_VERSION}\E(?![0-9.])/$1$ENV{NEW_VERSION}/g
      ' "$file"
  done < <(find docs -type f -name '*.md' -print0)
fi

# The section goes directly under the marker, followed by one empty line;
# the rest of the index stays as it is.
updated_index="$work_dir/index.md"
awk -v marker="$marker" -v section="$section_file" '
  { print }
  $0 == marker {
    while ((getline line < section) > 0) {
      print line
    }
    close(section)
    print ""
  }
' "$notes_index" >"$updated_index"
cat "$updated_index" >"$notes_index"

echo "Prepared $release_version ($bump) from $previous_tag."
# One line of JSON, so the output needs no multi-line delimiter.
release=$(
  jq -c -n \
    --arg version "$release_version" \
    --arg bump "$bump" \
    --arg previous_tag "$previous_tag" \
    --arg release_branch "$release_branch" \
    --arg prepare_branch "$prepare_branch" \
    --slurpfile range "$range_file" \
    '{
      version: $version,
      bump: $bump,
      previousTag: $previous_tag,
      releaseBranch: $release_branch,
      prepareBranch: $prepare_branch,
      range: $range[0]
    }'
)
{
  echo 'prepared=true'
  echo "version=$release_version"
  echo "previous-tag=$previous_tag"
  echo "release=$release"
} >>"$output_file"
