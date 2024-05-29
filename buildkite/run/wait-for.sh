#!/usr/bin/env bash
#
# Given some parameters it will wait for the given build in Buildkite if requested
#
# Parameters:
#  $1 -> the Buildkite Build URL. Mandatory.
#  $2 -> the Buildkite Build Web URL. Mandatory.
#  $3 -> the BK token. Mandatory.
#

set -euo pipefail

MSG="parameter missing."
URL=${1:?$MSG}
WEB_URL=${2:?$MSG}
BK_TOKEN=${3:?$MSG}

echo "::group::WaitFor"
STATE="running"

echo "Waiting for build $WEB_URL to run "
# https://buildkite.com/docs/pipelines/defining-steps#build-states
while [ "$STATE" == "running" ] || [ "$STATE" == "scheduled" ] || [ "$STATE" == "creating" ]; do
  RESP=$(curl \
    -H "Authorization: Bearer $BK_TOKEN" \
    --no-progress-meter \
    --retry 5 \
    --retry-delay 5 \
    --retry-all-errors \
    "$URL")
  STATE=$(echo "$RESP" | jq -r ".state")
  echo -n "."
  sleep 1
done
echo ""
echo "::endgroup::"

echo "state=${STATE}" >> "$GITHUB_OUTPUT"
if [ "$STATE" == "passed" ]; then
  echo "Build passed ($WEB_URL)"
  exit 0
else
  echo "Build did not pass, it's '$STATE'. Check the logs at $WEB_URL"
  exit 1
fi
