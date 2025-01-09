#!/usr/bin/env bash
# Environment variables:
#  PR_URL
#  REPOSITORY_URL
#  ADDITIONAL_LABELS
#  EXCLUDED_LABEL
#  DRY_RUN
#  RUNNER_DEBUG
#
# You can run this locally for testing purposes:
#
# $ REPOSITORY_URL=https://github.com/elastic/apm-server PR_URL=https://github.com/elastic/apm-server/pull/15035 EXCLUDED_LABEL=backport-* DRY_RUN=true sh mergify/labels-copier/copy.sh
#

set -eo pipefail

# Support debugging in GitHub actions when RUNNER_DEBUG is set.
if [ -n "$RUNNER_DEBUG" ] ; then
  set -x
fi

add_label() {
  local label=$1
  local pr_url=$2

  if [ "$DRY_RUN" == "true" ]; then
    echo ">> [dry-run]: $label will be added"
  else
    gh pr edit --add-label "$label" "$pr_url"
  fi
}

pr_number=$(gh pr view --json body -q ".body" "$PR_URL" | sed -n -e '/automatic backport of pull request/,/done/p' | cut -d"#" -f2 | cut -d" " -f1)
gh pr view --json labels -q '.labels[]|.name' ${REPOSITORY_URL}/pull/$pr_number | while read label ; do
  if [[ -z "$labels" ]] || [[ ",$labels," =~ ",$label," ]]; then
    if [[ -n "$EXCLUDED_LABEL" ]] && [[ $label =~ $EXCLUDED_LABEL ]]; then
      echo ">> $label is excluded and will not be added since matches '$EXCLUDED_LABEL'"
    else
      add_label "$label" "$PR_URL"
    fi
  fi
done
