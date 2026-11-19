#!/usr/bin/env bash
#
# Render the release-note JSON as the Markdown section for the repository's
# release-notes index.
#
# Usage: render-release-notes.sh <source-json> <version> <heading-anchor-base> <subsection-anchor-base>
#
# Arguments:
#   source-json             release-note JSON to validate and render
#   version                 release version in X.Y.Z form
#   heading-anchor-base     anchor base of the version heading
#   subsection-anchor-base  anchor base of the two subsections; EDOT iOS uses
#                           a different base for them than for the heading
#
# Environment:
#   RELEASE_REPOSITORY  owner/repository used in pull-request links
#                       (required). Not GITHUB_REPOSITORY: the runner owns the
#                       GITHUB_* variables and ignores an override.
#   RELEASE_DATE        date printed under the heading (default today in UTC,
#                       "Month D, YYYY"); set only to reproduce a past section
#
# Validates the JSON shape, refuses input that still has `uncategorized`
# items, has no items, or has a message that already starts with
# `[Breaking]` (the `breaking` flag is the only breaking signal, so the flag
# and the text cannot disagree), and prints a `## X.Y.Z` section: an
# untitled list for dependencies, then "Features and enhancements" and
# "Fixes" subsections. Empty groups are omitted. Items with `breaking: true`
# render with a `[Breaking]` prefix and sort first. The same section becomes
# the GitHub Release body.
#
# This script owns the section format. The prepare and finalize actions
# depend on its `## X.Y.Z ` heading: one inserts the section at the index
# marker and refuses a version that already has a heading, the other extracts
# the section by that heading as the Release body.

set -euo pipefail

if [[ $# -ne 4 ]]; then
  echo "Usage: render-release-notes.sh <source-json> <version> <heading-anchor-base> <subsection-anchor-base>" >&2
  exit 2
fi

source_file=$1
version=$2
heading_anchor_base=$3
subsection_anchor_base=$4
release_date=${RELEASE_DATE:-$(LC_ALL=C date -u +'%B %-d, %Y')}
repository=${RELEASE_REPOSITORY:-}

# The composite action marks these inputs required, but GitHub does not
# enforce that at run time; an empty value would render broken anchors or
# links without a word of complaint.
if [[ -z $heading_anchor_base ]]; then
  echo "Missing required heading-anchor-base." >&2
  exit 1
fi
if [[ -z $subsection_anchor_base ]]; then
  echo "Missing required subsection-anchor-base." >&2
  exit 1
fi
if [[ -z $repository ]]; then
  echo "Missing required repository (RELEASE_REPOSITORY) for pull-request links." >&2
  exit 1
fi

if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Invalid release version: $version" >&2
  exit 1
fi
if ! jq empty "$source_file" >/dev/null 2>&1; then
  echo "Release notes are not valid JSON: $source_file" >&2
  exit 1
fi
if ! jq -e '
  type == "object"
  and (.dependencies | type == "array")
  and (.featuresEnhancements | type == "array")
  and (.fixes | type == "array")
  and (.uncategorized | type == "array")
  and ([.dependencies[], .featuresEnhancements[], .fixes[], .uncategorized[]]
    | all(
        type == "object"
        and (.message | type == "string" and length > 0 and (test("[\\r\\n]") | not))
        and (.breaking == null or (.breaking | type == "boolean"))
        and (
          .prId == null
          or (.prId | type == "number" and . == floor and . > 0)
          or (.prId | type == "string" and test("^[1-9][0-9]*$"))
        )
      )
  )
' "$source_file" >/dev/null; then
  echo "Release notes must be a JSON object with dependencies, featuresEnhancements, fixes, and uncategorized arrays of items with a one-line message, an optional prId, and an optional boolean breaking." >&2
  exit 1
fi

if jq -e '[.dependencies[], .featuresEnhancements[], .fixes[], .uncategorized[]]
  | any(.message | startswith("[Breaking]"))' "$source_file" >/dev/null; then
  echo "Release-note messages must not start with [Breaking]; set breaking: true instead." >&2
  exit 1
fi
if [[ $(jq '.uncategorized | length' "$source_file") -ne 0 ]]; then
  echo "Release notes contain uncategorized items; place or delete every item before preparing the release." >&2
  exit 1
fi
if [[ $(jq '[.dependencies[], .featuresEnhancements[], .fixes[]] | length' "$source_file") -eq 0 ]]; then
  echo "Release notes must contain at least one item." >&2
  exit 1
fi

# One bullet per item, breaking items first: "* [Breaking] message: [#N](url)";
# the link part is omitted when the item has no prId.
render_items() {
  local filter=$1
  jq -r \
    --arg repository "$repository" \
    "$filter
     | sort_by(if .breaking == true then 0 else 1 end)
     | .[]
     | \"* \" + (if .breaking == true then \"[Breaking] \" else \"\" end) + .message
       + (if .prId == null then \"\"
          else \": [#\" + (.prId | tostring) + \"](https://github.com/\" + \$repository + \"/pull/\" + (.prId | tostring) + \")\"
          end)" \
    "$source_file"
}

# The docs site expects `<base>-release-notes` on the version heading and
# `<base>-features-enhancements` / `<base>-fixes` on the subsections, with
# whatever bases the repository's existing sections already use.
printf '## %s [%s-release-notes]\n' "$version" "$heading_anchor_base"
printf '**Release date:** %s\n' "$release_date"

if [[ $(jq '.dependencies | length' "$source_file") -gt 0 ]]; then
  printf '\n'
  render_items '.dependencies'
fi
if [[ $(jq '.featuresEnhancements | length' "$source_file") -gt 0 ]]; then
  printf '\n### Features and enhancements [%s-features-enhancements]\n\n' "$subsection_anchor_base"
  render_items '.featuresEnhancements'
fi
if [[ $(jq '.fixes | length' "$source_file") -gt 0 ]]; then
  printf '\n### Fixes [%s-fixes]\n\n' "$subsection_anchor_base"
  render_items '.fixes'
fi
