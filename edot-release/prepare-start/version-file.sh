#!/usr/bin/env bash
#
# Read or write the version in an EDOT SDK repository's version file. Every
# release action that needs the version goes through this script, so the
# rule for finding the version line has one home. The file and its line
# come from the repository's EDOT release configuration (config.sh):
# `versionFile`, and `versionLine` with one `{version}` placeholder.
#
# Usage:
#   version-file.sh read [commit]   print the version, from the working tree
#                                   or from the file at <commit>
#   version-file.sh write <version> set the version in the working tree;
#                                   <version> is X.Y.Z or X.Y.Z-SNAPSHOT
#
# The text before `{version}` is the line's prefix and the text after it the
# suffix. Exactly one line may start with the prefix and end with the
# suffix, so a reformatted file fails instead of being misread; the version
# is what lies between. Matching compares strings literally, so no character
# of the configured line has a special meaning. A write rebuilds that one
# line from prefix, version, and suffix and keeps every other line.

set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
version_file=$("$script_dir/config.sh" get versionFile)
version_line=$("$script_dir/config.sh" get versionLine)
# config.sh guarantees exactly one placeholder.
export VERSION_LINE_PREFIX=${version_line%%"{version}"*}
export VERSION_LINE_SUFFIX=${version_line#*"{version}"}

usage() {
  cat >&2 <<'USAGE'
Usage:
  version-file.sh read [commit]
  version-file.sh write <version>
USAGE
  exit 2
}

work_dir=$(mktemp -d "${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-version-file.XXXXXX")
trap 'rm -rf "$work_dir"' EXIT
export VERSION_LINE_REPORT="$work_dir/report"

# One awk program owns the match for both commands. The prefix, suffix, and
# new version arrive through ENVIRON, which, unlike awk -v, keeps
# backslashes as they are. It prints every line unchanged except the version
# line, which it rebuilds when NEW_VERSION is set, and writes the number of
# version lines and the version found to VERSION_LINE_REPORT.
match_version_line() {
  awk '
    BEGIN {
      prefix = ENVIRON["VERSION_LINE_PREFIX"]
      suffix = ENVIRON["VERSION_LINE_SUFFIX"]
    }
    length($0) >= length(prefix) + length(suffix) \
      && substr($0, 1, length(prefix)) == prefix \
      && substr($0, length($0) - length(suffix) + 1) == suffix {
      count++
      found = substr($0, length(prefix) + 1, length($0) - length(prefix) - length(suffix))
      if (ENVIRON["NEW_VERSION"] != "") {
        $0 = prefix ENVIRON["NEW_VERSION"] suffix
      }
    }
    { print }
    END { printf "%d\n%s\n", count, found > ENVIRON["VERSION_LINE_REPORT"] }
  '
}

# Stop unless the last match_version_line run found exactly one version line.
require_one_line() {
  local count
  count=$(sed -n 1p "$VERSION_LINE_REPORT")
  if [[ $count -ne 1 ]]; then
    echo "Expected exactly one line matching versionLine in $1, found $count." >&2
    exit 1
  fi
}

case ${1:-} in
  read)
    [[ $# -le 2 ]] || usage
    if [[ $# -eq 2 ]]; then
      git show "$2:$version_file" | NEW_VERSION='' match_version_line >/dev/null
      require_one_line "$version_file at $2"
    else
      NEW_VERSION='' match_version_line <"$version_file" >/dev/null
      require_one_line "$version_file"
    fi
    sed -n 2p "$VERSION_LINE_REPORT"
    ;;
  write)
    [[ $# -eq 2 ]] || usage
    if [[ ! $2 =~ ^[0-9]+\.[0-9]+\.[0-9]+(-SNAPSHOT)?$ ]]; then
      echo "Invalid version for $version_file: $2" >&2
      exit 1
    fi
    NEW_VERSION=$2 match_version_line <"$version_file" >"$work_dir/updated"
    # Replace the file only after the one-line rule held.
    require_one_line "$version_file"
    cat "$work_dir/updated" >"$version_file"
    ;;
  *)
    usage
    ;;
esac
