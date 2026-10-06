#!/usr/bin/env bash
#
# Read one field of the repository's EDOT release configuration. The
# prepare and publish actions take the platform facts of an EDOT SDK
# repository from this one file instead of from inputs, so a consumer states
# each fact once and every action reads it the same way.
#
# Usage: config.sh get <field>
#
# The file is `.github/edot-release.json` in the working directory, the
# checked-out commit. It is a JSON object with exactly these fields:
#   tagPrefix               release tag prefix, such as `v`; may be empty
#   productName             product name, such as `EDOT Android`
#   versionFile             path of the file that holds the version
#   versionLine             the version line with one `{version}` placeholder,
#                           matched literally, such as `version={version}`
#   appliesToKey            documentation `applies_to` key of the product
#   headingAnchorPrefix     anchor base of the version heading, without the
#                           version digits
#   subsectionAnchorPrefix  anchor base of the subsections, without the
#                           version digits
#   docsUrl                 published release-notes page
#   stagePaths              non-empty array of pathspecs to stage in the
#                           preparation commit; printed one per line
#
# The whole file is validated on every call, so any action stops on any
# mistake in it, with a message that names the file and the field.

set -euo pipefail

config_file=.github/edot-release.json

if [[ $# -ne 2 || $1 != get ]]; then
  echo "Usage: config.sh get <field>" >&2
  exit 2
fi
field=$2

if [[ ! -f $config_file ]]; then
  echo "$config_file not found; the repository must define its EDOT release configuration there." >&2
  exit 1
fi
if ! jq -e 'type == "object"' "$config_file" >/dev/null 2>&1; then
  echo "$config_file is not a JSON object." >&2
  exit 1
fi

# Collect every problem at once, so a consumer can fix the file in one pass.
problems=$(
  jq -r '
    def string_fields: ["tagPrefix", "productName", "versionFile", "versionLine",
      "appliesToKey", "headingAnchorPrefix", "subsectionAnchorPrefix", "docsUrl"];
    def fields: string_fields + ["stagePaths"];
    def one_line: type == "string" and (contains("\n") or contains("\r") | not);
    . as $config
    | (fields - keys | .[] | "missing key \(.)"),
      (keys - fields | .[] | "unknown key \(.)"),
      (string_fields[] as $key | select($config | has($key)) | $config[$key]
        | if one_line | not then "\($key) must be a one-line string"
          elif $key != "tagPrefix" and . == "" then "\($key) must not be empty"
          else empty end),
      (select(has("versionLine") and (.versionLine | type == "string"))
        | .versionLine | select(indices("{version}") | length != 1)
        | "versionLine must contain exactly one {version}"),
      (select(has("stagePaths")) | .stagePaths
        | if type != "array" then "stagePaths must be an array of pathspecs"
          elif length == 0 then "stagePaths must list at least one pathspec"
          elif any(.[]; (one_line and . != "") | not) then "stagePaths must hold non-empty one-line strings"
          else empty end)
  ' "$config_file"
)
if [[ -n $problems ]]; then
  while IFS= read -r problem; do
    echo "$config_file: $problem." >&2
  done <<<"$problems"
  exit 1
fi

if ! jq -e --arg field "$field" 'has($field)' "$config_file" >/dev/null; then
  echo "Unknown configuration field '$field'." >&2
  exit 2
fi
jq -r --arg field "$field" '.[$field] | if type == "array" then .[] else . end' "$config_file"
