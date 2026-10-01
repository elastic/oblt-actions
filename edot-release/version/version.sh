#!/usr/bin/env bash
#
# Version arithmetic for the EDOT release actions. Nobody types a version;
# every version is derived here from the highest release tag, so the tag
# pattern and the semantic-version rules have one home for every EDOT SDK
# repository. The repository supplies its tag prefix through TAG_PREFIX
# (`v` on EDOT Android, empty on EDOT iOS). Returned tags carry the prefix;
# returned versions do not.
#
#   highest-tag [line]                 the latest release tag by version order,
#                                      optionally restricted to X.Y
#   previous-tag [ref-name]            the release a new one from <ref-name>
#                                      follows: `X.Y.(Z-1)` for
#                                      `patching/X.Y.Z`, else highest-tag
#   next-patch <tag-or-version>        the next patch version
#   release-version <tag> <dev> <bump> the version to release; fails when
#                                      <dev> is not the next minor `-SNAPSHOT`
#                                      after <tag>, which catches an unmerged
#                                      release PR
#   next-development <version>         the next minor `-SNAPSHOT` after a
#                                      release version or tag
#
# Each argument may also arrive through an environment variable (LINE,
# REF_NAME, VERSION, PREVIOUS_TAG, DEVELOPMENT_VERSION, BUMP). That is how
# the composite action passes its inputs without interpolating them into
# shell source.

set -euo pipefail

tag_prefix=${TAG_PREFIX:-}

usage() {
  cat >&2 <<'USAGE'
Usage:
  version.sh highest-tag [line]
  version.sh previous-tag [ref-name]
  version.sh next-patch <release-version-or-tag>
  version.sh release-version <previous-tag> <development-version> <minor|major>
  version.sh next-development <release-version-or-tag>
USAGE
  exit 2
}

require_value() {
  if [[ -z $2 ]]; then
    echo "Missing $1." >&2
    usage
  fi
}

# One semantic-version component: 0 or an integer without a leading zero.
# A leading zero is invalid SemVer, and Bash would read it as octal in the
# arithmetic below, so it has to stop here with a readable message.
component='(0|[1-9][0-9]*)'

# The prefix is spliced into an extended regex below; escape it so a prefix
# with a metacharacter cannot widen the match.
regex_escape() {
  sed 's/[][(){}.^$*+?|\\/]/\\&/g' <<<"$1"
}

# Accept a tag or a bare version: strip the prefix only when present, then
# require exactly X.Y.Z so a prerelease or malformed value stops here.
parse_version() {
  local value=$1
  if [[ -n $tag_prefix && $value == "$tag_prefix"* ]]; then
    value=${value#"$tag_prefix"}
  fi
  if [[ ! $value =~ ^$component\.$component\.$component$ ]]; then
    echo "Invalid semantic version: $1" >&2
    exit 1
  fi
  VERSION_MAJOR=${BASH_REMATCH[1]}
  VERSION_MINOR=${BASH_REMATCH[2]}
  VERSION_PATCH=${BASH_REMATCH[3]}
}

next_development() {
  parse_version "$1"
  printf '%s.%s.0-SNAPSHOT\n' "$VERSION_MAJOR" "$((VERSION_MINOR + 1))"
}

command=${1:-}
case $command in
  highest-tag)
    [[ $# -le 2 ]] || usage
    line=${2-${LINE:-}}
    if [[ -n $line && ! $line =~ ^$component\.$component$ ]]; then
      echo "Invalid release line '$line'; expected X.Y." >&2
      exit 1
    fi
    # Only exact <prefix>X.Y.Z tags count. The glob alone would also match
    # names such as v2.0.0-rc1, or legacy v1.4.0 tags in a repository that
    # has moved to plain tags, and make preparation fail on them.
    escaped_prefix=$(regex_escape "$tag_prefix")
    pattern="^${escaped_prefix}${component}\\.${component}\\.${component}$"
    if [[ -n $line ]]; then
      pattern="^${escaped_prefix}${line//./\\.}\\.${component}$"
    fi
    tag=$(
      git tag --list "${tag_prefix}*" --sort=-version:refname \
        | grep -E "$pattern" \
        | head -n 1 \
        || true
    )
    if [[ -z $tag ]]; then
      if [[ -n $line ]]; then
        echo "No release exists on line $line." >&2
        exit 1
      fi
      echo "No release tag matching ${tag_prefix}X.Y.Z was found." >&2
      exit 1
    fi
    parse_version "$tag"
    printf '%s\n' "$tag"
    ;;
  previous-tag)
    [[ $# -le 2 ]] || usage
    ref_name=${2-${REF_NAME:-}}
    if [[ $ref_name != patching/* ]]; then
      exec "$0" highest-tag
    fi
    # A patch branch is named after the version it will release, so its
    # previous release is the same line one patch lower. A zero patch digit
    # would make that previous release a minor, which the branch cannot be.
    if [[ ! ${ref_name#patching/} =~ ^$component\.$component\.([1-9][0-9]*)$ ]]; then
      echo "Patch branch '$ref_name' must end in X.Y.Z with a nonzero patch version." >&2
      exit 1
    fi
    printf '%s%s.%s.%s\n' "$tag_prefix" "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}" "$((BASH_REMATCH[3] - 1))"
    ;;
  next-patch)
    [[ $# -le 2 ]] || usage
    version=${2-${VERSION:-}}
    require_value version "$version"
    parse_version "$version"
    printf '%s.%s.%s\n' "$VERSION_MAJOR" "$VERSION_MINOR" "$((VERSION_PATCH + 1))"
    ;;
  release-version)
    [[ $# -le 4 ]] || usage
    previous_tag=${2-${PREVIOUS_TAG:-}}
    development_version=${3-${DEVELOPMENT_VERSION:-}}
    bump=${4-${BUMP:-}}
    require_value previous-tag "$previous_tag"
    require_value development-version "$development_version"
    require_value bump "$bump"
    # The version file must hold the next minor -SNAPSHOT after the previous
    # tag. Anything else means the previous release's PR into main has not
    # merged yet, and releasing on top of it would skip or repeat a version.
    expected=$(next_development "$previous_tag")
    if [[ $development_version != "$expected" ]]; then
      echo "Expected development version $expected after $previous_tag, found $development_version." >&2
      exit 1
    fi
    parse_version "$previous_tag"
    case $bump in
      minor)
        printf '%s.%s.0\n' "$VERSION_MAJOR" "$((VERSION_MINOR + 1))"
        ;;
      major)
        printf '%s.0.0\n' "$((VERSION_MAJOR + 1))"
        ;;
      *)
        echo "Unsupported bump '$bump'; expected minor or major." >&2
        exit 1
        ;;
    esac
    ;;
  next-development)
    [[ $# -le 2 ]] || usage
    version=${2-${VERSION:-}}
    require_value version "$version"
    next_development "$version"
    ;;
  '')
    usage
    ;;
  *)
    echo "Unknown command '$command'." >&2
    usage
    ;;
esac
