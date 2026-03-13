#!/usr/bin/env bash
#
# Given some parameters it will wait for the given build in Buildkite if requested
#
# Environment variables:
#  BK_TOKEN -> the BK token. Mandatory.
#  URL      -> the Buildkite Build URL. Mandatory.
#  WEB_URL  -> the Buildkite Build Web URL. Mandatory.
#

set -euo pipefail

MSG="environment variable missing."
BK_TOKEN=${BK_TOKEN:?$MSG}
URL=${URL:?$MSG}
WEB_URL=${WEB_URL:?$MSG}

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
