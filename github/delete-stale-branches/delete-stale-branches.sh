#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:?REPO is required}"
STALE_MONTHS="${STALE_MONTHS:-36}"
DRY_RUN="${DRY_RUN:-true}"

if [[ ! "${REPO}" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]]; then
  echo "::error::repository must be in owner/name format"
  exit 1
fi
if [[ ! "${STALE_MONTHS}" =~ ^[1-9][0-9]*$ ]]; then
  echo "::error::stale-months must be a positive integer"
  exit 1
fi
if [[ "${DRY_RUN}" != "true" && "${DRY_RUN}" != "false" ]]; then
  echo "::error::dry-run must be true or false"
  exit 1
fi

OWNER="${REPO%%/*}"
NAME="${REPO##*/}"

if date --version >/dev/null 2>&1; then
  CUTOFF="$(date -u -d "${STALE_MONTHS} months ago" +%Y-%m-%dT%H:%M:%SZ)"
else
  CUTOFF="$(date -u -v-"${STALE_MONTHS}"m +%Y-%m-%dT%H:%M:%SZ)"
fi
echo "Repo: ${REPO} | cutoff: ${CUTOFF} | dry run: ${DRY_RUN}"

DEFAULT_BRANCH="$(gh api "repos/${REPO}" --jq .default_branch)"

OPEN_PR_BRANCHES="$(gh pr list -R "${REPO}" --state open --limit 5000 \
  --json headRefName,isCrossRepository --jq '.[] | select(.isCrossRepository | not) | .headRefName')"

BRANCHES="$(gh api graphql --paginate \
  -f owner="${OWNER}" -f name="${NAME}" \
  -f query='query($owner:String!,$name:String!,$endCursor:String){
    repository(owner:$owner,name:$name){
      refs(refPrefix:"refs/heads/",first:100,after:$endCursor){
        pageInfo{hasNextPage endCursor}
        nodes{name branchProtectionRule{id} target{... on Commit{committedDate}}}
      }
    }
  }' --jq '.data.repository.refs.nodes[] | [.name, .target.committedDate, (.branchProtectionRule != null)] | @tsv')"

RELEASE_RE='^([0-9]+\.([0-9]+|x))$'
count=0
while IFS=$'\t' read -r branch date protected; do
  [[ -z "${branch}" || -z "${date}" ]] && continue
  [[ "${branch}" == "${DEFAULT_BRANCH}" ]] && continue
  [[ "${protected}" == "true" ]] && continue
  [[ "${branch}" =~ ${RELEASE_RE} ]] && continue
  [[ ! "${date}" < "${CUTOFF}" ]] && continue
  if grep -Fxq -- "${branch}" <<<"${OPEN_PR_BRANCHES}"; then
    continue
  fi

  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "[dry-run] would delete ${branch} (last commit ${date})"
  else
    echo "Deleting ${branch} (last commit ${date})"
    gh api -X DELETE "repos/${REPO}/git/refs/heads/${branch}" >/dev/null \
      || { echo "::warning::Failed to delete ${branch}"; continue; }
  fi
  count=$((count + 1))
done <<<"${BRANCHES}"

echo "Stale branches $([[ "${DRY_RUN}" == "true" ]] && echo "found" || echo "deleted"): ${count}"
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "stale-branches-count=${count}" >> "${GITHUB_OUTPUT}"
fi
