#!/usr/bin/env bash
#
# Read or write the version in an EDOT SDK repository's version file. Every
# release action that needs the version goes through this script, so the
# rule for finding the version line has one home: the repository supplies
# the file and a Perl regex for its version line with exactly one capture
# group around the version.
#
# Usage:
#   version-file.sh read [commit]   print the version, from the working tree
#                                   or from the file at <commit>
#   version-file.sh write <version> set the version in the working tree;
#                                   <version> is X.Y.Z or X.Y.Z-SNAPSHOT
#
# Environment:
#   VERSION_FILE   path of the version file, relative to the repository root
#                  (required)
#   VERSION_REGEX  Perl regex matching the version line, with one capture
#                  group around the version (required)
#
# Exactly one line must match, so a reformatted file fails instead of being
# misread. A write replaces only the capture group's span and keeps the rest
# of the line byte for byte.

set -euo pipefail

version_file=${VERSION_FILE:?VERSION_FILE is required}
label=$version_file
: "${VERSION_REGEX:?VERSION_REGEX is required}"

usage() {
  cat >&2 <<'USAGE'
Usage:
  version-file.sh read [commit]
  version-file.sh write <version>
USAGE
  exit 2
}

# Print the captured version from the file content on standard input; the
# argument names that content in the error message. The regex arrives
# through the environment, so no quoting reaches Perl source.
read_version() {
  VERSION_FILE_LABEL=$1 perl -e '
    my $regex = qr/$ENV{VERSION_REGEX}/;
    my ($count, $value) = (0, undef);
    while (my $line = <STDIN>) {
      chomp $line;
      if ($line =~ $regex) {
        $count++;
        $value = $1;
      }
    }
    if ($count != 1) {
      print STDERR "Expected exactly one line matching the version regex in $ENV{VERSION_FILE_LABEL}, found $count.\n";
      exit 1;
    }
    if (!defined $value) {
      print STDERR "The version regex has no capture group around the version.\n";
      exit 1;
    }
    print "$value\n";
  '
}

case ${1:-} in
  read)
    [[ $# -le 2 ]] || usage
    if [[ $# -eq 2 ]]; then
      git show "$2:$version_file" | read_version "$version_file at $2"
    else
      read_version "$label" <"$version_file"
    fi
    ;;
  write)
    [[ $# -eq 2 ]] || usage
    if [[ ! $2 =~ ^[0-9]+\.[0-9]+\.[0-9]+(-SNAPSHOT)?$ ]]; then
      echo "Invalid version for $version_file: $2" >&2
      exit 1
    fi
    # Check the one-line rule before touching the file.
    read_version "$label" <"$version_file" >/dev/null
    # Replace the bytes between the start and end of capture group 1 on the
    # matching line; everything around them, including the line ending, stays.
    NEW_VERSION=$2 perl -pi -e '
      BEGIN { $regex = qr/$ENV{VERSION_REGEX}/ }
      if (/$regex/) {
        substr($_, $-[1], $+[1] - $-[1]) = $ENV{NEW_VERSION};
      }
    ' "$version_file"
    ;;
  *)
    usage
    ;;
esac
