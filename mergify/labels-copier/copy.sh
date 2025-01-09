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

# Get the PR Number from the body since Mergify uses the PR number as the body.
pr_number=$(gh pr view --json body -q ".body" "$PR_URL" | sed -n -e '/automatic backport of pull request/,/done/p' | cut -d"#" -f2 | cut -d" " -f1)

# Get the labels from the PR and filter out the excluded labels.
labels=$(gh pr view --json labels "${REPOSITORY_URL}/pull/$pr_number" | jq -r --arg regex "$EXCLUDED_LABEL" '.labels | map(select(.name | test($regex) | not)) | map(.name) | join(",")')

echo ">> $labels will be added"
if [ "$DRY_RUN" == "true" ]; then
  echo ">> DRY_RUN is set, skipping the label addition"
else
  gh pr edit --add-label "$labels" "$PR_URL"
fi
