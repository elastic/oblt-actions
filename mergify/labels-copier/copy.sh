#!/usr/bin/env bash
# Environment variables:
#  PR_URL
#  REPOSITORY
#  REPOSITORY_URL
#  EXCLUDED_LABEL
#  DRY_RUN
#  RUNNER_DEBUG
#
# You can run this locally for testing purposes:
#
# $ REPOSITORY=elastic/apm-server REPOSITORY_URL=https://github.com/elastic/apm-server PR_URL=https://github.com/elastic/apm-server/pull/15035 EXCLUDED_LABEL=backport-* DRY_RUN=true sh mergify/labels-copier/copy.sh
#

set -eo pipefail

# Support debugging in GitHub actions when RUNNER_DEBUG is set.
if [ -n "$RUNNER_DEBUG" ] ; then
  set -x
fi

# Get the PR Number from the body since Mergify uses the PR number as the body.
pr_number=$(gh pr view --json body -q ".body" "$PR_URL" --repo "$REPOSITORY" \
  | sed -n -e '/automatic backport of pull request/,/done/p' \
  | sed 's#.*automatic backport of pull request ##g' \
  | cut -d"#" -f2 \
  | cut -d" " -f1)

# Get the labels from the PR and filter out the excluded labels.
labels=$(gh pr view --json labels "${REPOSITORY_URL}/pull/$pr_number" --repo "$REPOSITORY" | jq -r --arg regex "$EXCLUDED_LABEL" '.labels | map(select(.name | test($regex) | not)) | map(.name) | join(",")')
if [ -n "$CI" ] ; then
  echo "labels=$labels" >> "$GITHUB_OUTPUT"
fi
echo ">> $labels will be added"
if [ "$DRY_RUN" == "true" ]; then
  echo ">> DRY_RUN is set, skipping the label addition"
else
  gh pr edit --add-label "$labels" "$PR_URL"
fi
