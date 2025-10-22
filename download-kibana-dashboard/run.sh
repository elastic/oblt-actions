#!/usr/bin/env bash
#
set -euo pipefail

# Use environment variables, with sensible defaults if not set
KIBANA_HOST="${KIBANA_HOST:?KIBANA_HOST is required}"
KIBANA_USER="${KIBANA_USER:?KIBANA_USER is required}"
KIBANA_PASSWORD="${KIBANA_PASSWORD:?KIBANA_PASSWORD is required}"
FROM_DATE="${FROM_DATE:?FROM_DATE is required}"
TO_DATE="${TO_DATE:?TO_DATE is required}"
DASHBOARD_ID="${DASHBOARD_ID:-kibana-dashboard}"
PNG_OUTPUT_FILE="${PNG_OUTPUT_FILE:-out.png}"
TABLE_WIDTH="${TABLE_WIDTH:-2400}"
MAX_ATTEMPTS="${MAX_ATTEMPTS:-20}"

# Mask secrets in GitHub logs
echo "::add-mask::$KIBANA_USER"
echo "::add-mask::$KIBANA_HOST"
echo "::add-mask::$KIBANA_PASSWORD"

VERSION="0.0.0" # mandatory, doesn't do anything

JOB_PARAMS=$(echo "
(
  layout:(
    dimensions:(
      height:400,
      width:${TABLE_WIDTH}
    ),id:preserve_layout
  ),
  locatorParams:(
    id:DASHBOARD_APP_LOCATOR,
    params:(
      dashboardId:'${DASHBOARD_ID}',
      preserveSavedFilters:!t,
      query:(language:kuery,query:''),
      timeRange:(
        from:'${FROM_DATE}',
        to:'${TO_DATE}'
      ),
      useHash:!f,
      viewMode:view
    )
  ),
  objectType:dashboard,
  title:'ecf_gcp',
  version:'${VERSION}'
)
" | tr -d "[:space:]")

# Request report generation
response=$(curl -sSL -u "$KIBANA_USER:$KIBANA_PASSWORD" \
  -H 'kbn-xsrf: true' \
  --data-urlencode "jobParams=${JOB_PARAMS}" "$KIBANA_HOST/api/reporting/generate/pngV2"
)
png_url_path=$(echo "$response" | jq -r '.path')

if [[ "$png_url_path" == "null" || -z "$png_url_path" ]]; then
  echo "Failed to queue report. Response:"
  echo "$response"
  exit 1
fi
echo "PNG URL path: $png_url_path"

attempt_counter=0
sleep_timeout=10
# Poll for report readiness, handle 503 Retry-After
while true; do
  http_code=$(curl -s -o /dev/null -w "%{http_code}" -u "$KIBANA_USER:$KIBANA_PASSWORD" -H 'kbn-xsrf: true' "$KIBANA_HOST$png_url_path")
  if [[ "$http_code" == "200" ]]; then
    echo "Report is ready!"
    break
  elif [[ "$http_code" == "500" ]]; then
    echo "Report generation failed (HTTP 500)."
    exit 1
  elif [[ "$http_code" == "503" ]]; then
    # Check for Retry-After header
    retry_after=$(curl -sI -u "$KIBANA_USER:$KIBANA_PASSWORD" -H 'kbn-xsrf: true' "$KIBANA_HOST$png_url_path" | grep -i 'Retry-After:' | awk '{print $2}' | tr -d '\r')
    if [[ -n "$retry_after" ]]; then
      echo "Report not ready, waiting $retry_after seconds (from Retry-After header)..."
      sleep "$retry_after"
    else
      echo "Report not ready, waiting $sleep_timeout seconds..."
      sleep "$sleep_timeout"
    fi
  else
    echo "Unexpected HTTP code: $http_code"
    exit 1
  fi

  attempt_counter=$((attempt_counter+1))
  if (( attempt_counter >= MAX_ATTEMPTS )); then
    echo "Max attempts reached. PNG report timed out."
    exit 1
  fi
done

echo "Downloading PNG report to $PNG_OUTPUT_FILE..."
curl -sSL --output "$PNG_OUTPUT_FILE" -u "$KIBANA_USER:$KIBANA_PASSWORD" -H 'kbn-xsrf: true' "$KIBANA_HOST$png_url_path"
echo "PNG report downloaded successfully."
