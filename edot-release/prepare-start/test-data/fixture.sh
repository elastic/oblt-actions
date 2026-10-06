#!/usr/bin/env bash
#
# Build and check the fixture repository that the edot-release flow-action
# and start-patch test workflows run against. One builder serves all five
# workflows, so the fixture layout has one home.
#
# The fixture is a Git repository at GITHUB_WORKSPACE, next to the
# oblt-actions checkout in `oblt-actions/` (excluded through
# .git/info/exclude), so the actions' relative paths resolve in the fixture.
# Its `origin` is a bare repository in RUNNER_TEMP, so nothing a test does
# can reach GitHub through Git.
#
# Usage:
#   fixture.sh create <layout> <version> <tag> [<trailer-sha>]
#       Replace the fixture with a fresh one. <layout> is android or ios: the
#       EDOT release configuration, version file, release-notes index, and
#       applies_to page of that platform from test-data/<layout>/. Commits
#       them with the version file at <version>, tags the commit <tag>, and,
#       with <trailer-sha>, adds an empty commit whose
#       `(cherry picked from commit <trailer-sha>)` trailer makes pr-range
#       resolve it to that commit's pull request.
#       Pushes `main` and the tag to the bare origin and takes a snapshot.
#   fixture.sh set-version <version>     set the version file in the tree
#   fixture.sh config <jq-filter>        rewrite the configuration in the
#                                        tree through a jq filter
#   fixture.sh duplicate-version-line    append a second version line
#   fixture.sh add-section <version>     insert a minimal release section for
#                                        <version> under the index marker
#   fixture.sh commit <message> [<trailer-sha>]
#                                        commit the tree and print the SHA
#   fixture.sh import <repository> <sha> fetch a commit of a public GitHub
#                                        repository and its parents into the
#                                        fixture, creating no ref
#   fixture.sh remote-branch <branch>    create <branch> at HEAD on the origin
#                                        only; take a snapshot after it
#   fixture.sh compare <file> <expected> diff a file against an expected
#                                        one, ignoring the release date and
#                                        trailing whitespace
#   fixture.sh snapshot                  record the origin's refs, the local
#                                        branches, tags, and HEAD, and the
#                                        working tree status
#   fixture.sh check-unchanged           fail unless all of that still
#                                        matches the snapshot
#   fixture.sh check-origin              fail unless the origin's refs still
#                                        match the snapshot
#   fixture.sh forget-identity           remove the fixture's Git identity
#                                        and stop Git from guessing one
#   fixture.sh check-upstream <repository> <version>...
#                                        fail if <repository> has a branch,
#                                        tag, Release, or pull request that a
#                                        dry-run for <version> must not create,
#                                        patch branches included
#
# Environment: GITHUB_WORKSPACE and RUNNER_TEMP (required); GH_TOKEN for
# check-upstream.

set -euo pipefail

test_data=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
workspace=${GITHUB_WORKSPACE:?GITHUB_WORKSPACE is required}
origin="${RUNNER_TEMP:?RUNNER_TEMP is required}/edot-release-fixture-origin.git"
snapshot="$RUNNER_TEMP/edot-release-fixture.state"
index=docs/release-notes/index.md
marker='% next_release_notes'

cd "$workspace"

layout() {
  cat .git/edot-release-fixture-layout
}

version_file() {
  case $(layout) in
    android) echo gradle.properties ;;
    ios) echo Sources/apm-agent-ios/Version.swift ;;
  esac
}

set_version() {
  case $(layout) in
    android)
      VALUE=$1 perl -pi -e 's/^version=.*/version=$ENV{VALUE}/' gradle.properties
      ;;
    ios)
      VALUE=$1 perl -pi -e 's/(elasticSwiftAgentVersion: String = ")[^"]*/$1$ENV{VALUE}/' \
        Sources/apm-agent-ios/Version.swift
      ;;
  esac
}

commit() {
  local message=$1 trailer=${2:-}
  git add -A
  if [[ -n $trailer ]]; then
    git commit --quiet --allow-empty -m "$message" -m "(cherry picked from commit $trailer)"
  else
    git commit --quiet --allow-empty -m "$message"
  fi
  git rev-parse HEAD
}

# The state a test compares before and after a case: the origin's refs, the
# local branches and tags, the checked-out branch, and the working tree and
# index status. Remote-tracking refs are left out; fetches may update them.
state() {
  echo '# origin'
  git ls-remote origin
  echo '# local'
  git for-each-ref --format='%(objectname) %(refname)' refs/heads refs/tags
  echo "# HEAD $(git symbolic-ref -q HEAD || git rev-parse HEAD)"
  echo '# status'
  git status --porcelain
}

take_snapshot() {
  state >"$snapshot"
}

case ${1:-} in
  create)
    [[ $# -ge 4 && $# -le 5 ]] || { echo "Usage: fixture.sh create <layout> <version> <tag> [<trailer-sha>]" >&2; exit 2; }
    fixture_layout=$2
    [[ -d $test_data/$fixture_layout ]] || { echo "Unknown layout '$fixture_layout'." >&2; exit 2; }
    [[ -d $workspace/oblt-actions ]] || { echo "Expected the oblt-actions checkout in $workspace/oblt-actions." >&2; exit 2; }
    # Start from nothing but the oblt-actions checkout.
    find "$workspace" -mindepth 1 -maxdepth 1 ! -name oblt-actions -exec rm -rf {} +
    rm -rf "$origin"
    git init --quiet --bare "$origin"
    git init --quiet --initial-branch=main
    echo 'oblt-actions/' >>.git/info/exclude
    echo "$fixture_layout" >.git/edot-release-fixture-layout
    git config user.name 'EDOT release fixture'
    git config user.email 'edot-release-fixture@example.invalid'
    git remote add origin "$origin"
    mkdir -p .github docs/release-notes docs/reference
    cp "$test_data/$fixture_layout/edot-release.json" .github/edot-release.json
    cp "$test_data/$fixture_layout/index.md" "$index"
    cp "$test_data/$fixture_layout/applies-to.md" docs/reference/applies-to.md
    case $fixture_layout in
      android) cp "$test_data/android/gradle.properties" gradle.properties ;;
      ios)
        mkdir -p Sources/apm-agent-ios
        cp "$test_data/ios/Version.swift" Sources/apm-agent-ios/Version.swift
        ;;
    esac
    set_version "$3"
    commit "Release $4" >/dev/null
    git tag "$4"
    if [[ $# -eq 5 ]]; then
      commit 'Fixture change' "$5" >/dev/null
    fi
    git push --quiet origin refs/heads/main:refs/heads/main "refs/tags/$4:refs/tags/$4"
    take_snapshot
    ;;
  set-version)
    [[ $# -eq 2 ]] || exit 2
    set_version "$2"
    ;;
  config)
    [[ $# -eq 2 ]] || exit 2
    jq "$2" .github/edot-release.json >"$RUNNER_TEMP/edot-release-fixture-config.json"
    mv "$RUNNER_TEMP/edot-release-fixture-config.json" .github/edot-release.json
    ;;
  duplicate-version-line)
    [[ $# -eq 1 ]] || exit 2
    file=$(version_file)
    case $(layout) in
      android) line=$(grep '^version=' "$file") ;;
      ios) line=$(grep 'elasticSwiftAgentVersion: String' "$file") ;;
    esac
    printf '%s\n' "$line" >>"$file"
    ;;
  add-section)
    [[ $# -eq 2 ]] || exit 2
    # The same layout prepare-start writes: the section directly under the
    # marker, then one empty line.
    MARKER=$marker SECTION_VERSION=$2 SECTION_DIGITS=${2//./} perl -pi -e '
      if ($_ eq "$ENV{MARKER}\n") {
        $_ .= "## $ENV{SECTION_VERSION} [fixture-$ENV{SECTION_DIGITS}-release-notes]\n"
          . "**Release date:** October 5, 2026\n\n"
          . "* Fixture change: [#1135](https://github.com/elastic/oblt-actions/pull/1135)\n\n";
      }
    ' "$index"
    ;;
  commit)
    [[ $# -ge 2 && $# -le 3 ]] || exit 2
    commit "$2" "${3:-}"
    ;;
  import)
    [[ $# -eq 3 ]] || exit 2
    # Depth 2 brings the commit's parents too, so a test can count them. A
    # fetch by SHA creates no ref; the snapshot records neither FETCH_HEAD
    # nor the shallow boundary it writes.
    git fetch --quiet --depth=2 "https://github.com/$2.git" "$3"
    ;;
  remote-branch)
    [[ $# -eq 2 ]] || exit 2
    git push --quiet origin "HEAD:refs/heads/$2"
    ;;
  snapshot)
    take_snapshot
    ;;
  compare)
    [[ $# -eq 3 ]] || exit 2
    # The release date is the run date, and the copied indexes carry trailing
    # whitespace that the repository's hooks strip from the expected files.
    normalize() {
      sed -E -e 's/^\*\*Release date:\*\* .*/**Release date:** <date>/' -e 's/[[:space:]]+$//' "$1"
    }
    # diff of two process substitutions cannot see a sed failure, so a
    # missing file must stop here instead of comparing two empty streams.
    for file in "$2" "$3"; do
      [[ -f $file ]] || { echo "Missing $file." >&2; exit 1; }
    done
    diff <(normalize "$2") <(normalize "$3")
    ;;
  check-unchanged)
    if ! state | diff "$snapshot" -; then
      echo "The fixture changed since its snapshot." >&2
      exit 1
    fi
    ;;
  check-origin)
    if ! git ls-remote origin | diff <(sed -n '/^# origin$/,/^# local$/p' "$snapshot" | sed '1d;$d') -; then
      echo "The fixture origin changed since its snapshot." >&2
      exit 1
    fi
    ;;
  forget-identity)
    [[ $# -eq 1 ]] || exit 2
    git config --unset user.name
    git config --unset user.email
    git config user.useConfigOnly true
    ;;
  check-upstream)
    [[ $# -ge 3 ]] || exit 2
    repository=$2
    shift 2
    failed=false
    for version in "$@"; do
      major=${version%%.*}
      for ref in "heads/releasing/$major." "heads/prepare/$major." "heads/patch-notes/$major." "heads/patching/$major." "tags/v$major."; do
        found=$(gh api "repos/$repository/git/matching-refs/$ref" --jq '.[].ref')
        if [[ -n $found ]]; then
          echo "$repository has $found." >&2
          failed=true
        fi
      done
      found=$(gh api --paginate "repos/$repository/releases" --jq ".[] | select(.tag_name | startswith(\"v$major.\")) | .tag_name")
      if [[ -n $found ]]; then
        echo "$repository has Release $found." >&2
        failed=true
      fi
      for head in "releasing/$version" "prepare/$version" "patch-notes/$version" "patching/$version"; do
        found=$(gh pr list --repo "$repository" --state all --head "$head" --json url --jq '.[].url')
        if [[ -n $found ]]; then
          echo "$repository has a pull request from $head: $found" >&2
          failed=true
        fi
      done
    done
    [[ $failed == false ]]
    ;;
  *)
    echo "Unknown command '${1:-}'." >&2
    exit 2
    ;;
esac
