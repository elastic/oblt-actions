#!/usr/bin/env bash
# Check release freeze
#
# Reads release-freezes.json from the repository root or the variable FEATURE_FREEZE_FILE
# and compares the current  date against all freeze periods and outputs  "true"
# if there is a description for the current date, "false" otherwise.
# The file must contain a JSON array of freeze periods with structure:
# [{"begin": "YYYY-MM-DD", "end": "YYYY-MM-DD", "description": "string"}, ...]
#
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

IN_FREEZE=false
if [ -n "$FREEZE_DESC" ]; then
  IN_FREEZE=true
fi

echo "in-freeze=${IN_FREEZE}" >> "$GITHUB_OUTPUT"
echo "### Freeze Feature is ${IN_FREEZE}" >> "$GITHUB_STEP_SUMMARY"
