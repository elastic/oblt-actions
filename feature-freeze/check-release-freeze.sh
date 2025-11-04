#!/usr/bin/env bash
# Check release freeze
#
# Reads freeze periods from the file specified by the FEATURE_FREEZE_FILE environment variable,
# which defaults to 'release-freezes.json' in the repository root if not set.
# Compares the current date against all freeze periods and outputs "true"
# if there is a description for the current date, "false" otherwise.
# The file must contain a JSON array of freeze periods with structure:
# [{"begin": "YYYY-MM-DD", "end": "YYYY-MM-DD", "description": "string"}, ...]
# The date can be overridden by setting the CURRENT_DATE environment variable
# (for testing!). If not set, it defaults to the current date.

set -euo pipefail

CURRENT_DATE="${CURRENT_DATE:-$(date +%Y-%m-%d)}"
FEATURE_FREEZE_FILE="${FEATURE_FREEZE_FILE:-release-freezes.json}"

FREEZE_DESC=$(jq -r --arg current "$CURRENT_DATE" '
  .[] |
  select(.begin <= $current and .end >= $current) |
  .description
' "$FEATURE_FREEZE_FILE")

FREEZE_MESSAGE="not active"
IN_FREEZE=false
if [ -n "$FREEZE_DESC" ]; then
  IN_FREEZE=true
  FREEZE_MESSAGE="active"
fi

if [ -n "${CI:-}" ]; then
  echo "in-freeze=${IN_FREEZE}" >> "$GITHUB_OUTPUT"
  echo "::warning::Feature freeze is ${FREEZE_MESSAGE} during ${CURRENT_DATE}"
  echo "### Feature freeze is ${FREEZE_MESSAGE} during ${CURRENT_DATE}" >> "$GITHUB_STEP_SUMMARY"
fi
