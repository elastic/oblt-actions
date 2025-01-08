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

if [ -n "$RUNNER_DEBUG" ] ; then
  set -x
fi

pr_number=$(gh pr view --json body -q ".body" "$PR_URL" | sed -n -e '/automatic backport of pull request/,/done/p' | cut -d"#" -f2 | cut -d" " -f1)
gh pr view --json labels -q '.labels[]|.name' ${REPOSITORY_URL}/pull/$pr_number | while read label ; do
  if [[ -z "$labels" ]] || [[ ",$labels," =~ ",$label," ]]; then
    # Check if the label is excluded by regex
    excluded=false
    if [[ $label =~ $EXCLUDED_LABEL ]]; then
      excluded=true
    fi
    if [ "$excluded" == "false" ] ; then
      if [ "$DRY_RUN" == "true" ] ; then
        echo ">>> $label"
      else
        gh pr edit --add-label "$label" "$PR_URL"
      fi
    fi
  fi
  for additional_label in $(echo $ADDITIONAL_LABELS | sed "s/,/ /g") ; do
    if [ "$DRY_RUN" == "true" ] ; then
      echo ">>> $additional_label"
    else
      gh pr edit --add-label "$additional_label" "$PR_URL"
    fi
  done
done
