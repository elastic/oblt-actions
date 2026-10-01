#!/usr/bin/env bash
#
# Draft the release-note JSON for the next release.
#
# Usage: draft-release-notes.sh [ref] [previous-tag]
#
# Arguments:
#   ref           commit or ref to draft for (default HEAD)
#   previous-tag  release tag at the start of the range (default the tag
#                 Prepare release uses for RELEASE_REF_NAME, so a draft from
#                 a patch branch covers only that line's changes)
#
# Environment:
#   RELEASE_REF_NAME   branch the release is prepared from (default main)
#   RELEASE_REPOSITORY, GH_TOKEN, TAG_PREFIX  see ../pr-range/pr-range.sh
#
# Lists the pull requests merged since the previous release (see
# ../pr-range/pr-range.sh) and groups them with group.jq into the JSON shape
# that Prepare release accepts: `dependencies`, `featuresEnhancements`,
# `fixes`, and `uncategorized`. Labels are hints only. A PR with none of the
# three labels lands in `uncategorized` for the operator to place or delete.
# Repeated updates of the same dependency collapse into the last one merged.
# The output is a starting point; the operator edits it before dispatching.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
previous_tag=${2:-}
if [[ -z $previous_tag ]]; then
  previous_tag=$("$script_dir/../version/version.sh" previous-tag "${RELEASE_REF_NAME:-}")
fi
range=$("$script_dir/../pr-range/pr-range.sh" "${1:-HEAD}" "$previous_tag")

jq -f "$script_dir/group.jq" <<<"$range"
