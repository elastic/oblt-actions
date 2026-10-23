#!/usr/bin/env bash
set -euo pipefail

REPO="${REPO:?REPO is required}"
STALE_MONTHS="${STALE_MONTHS:-36}"
DRY_RUN="${DRY_RUN:-true}"
DEBUG="${DEBUG:-false}"

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
if [[ "${DEBUG}" != "true" && "${DEBUG}" != "false" ]]; then
  echo "::error::debug must be true or false"
  exit 1
fi

if [[ "${DEBUG}" == "true" ]]; then
  set -x
fi

if date --version >/dev/null 2>&1; then
  CUTOFF="$(date -u -d "${STALE_MONTHS} months ago" +%Y-%m-%dT%H:%M:%SZ)"
else
  CUTOFF="$(date -u -v-"${STALE_MONTHS}"m +%Y-%m-%dT%H:%M:%SZ)"
fi
echo "Repo: ${REPO} | cutoff: ${CUTOFF} | dry run: ${DRY_RUN}"

OWNER="${REPO%%/*}"
NAME="${REPO##*/}"

DEFAULT_BRANCH="$(gh api "repos/${REPO}" --jq .default_branch)"

PROTECTED_BRANCHES="$(gh api --method GET --paginate "repos/${REPO}/branches" \
  -f protected=true -f per_page=100 --jq '.[].name')"

BRANCHES="$(gh api graphql --paginate \
  -f owner="${OWNER}" -f name="${NAME}" \
  -f query='query($owner:String!,$name:String!,$endCursor:String){
    repository(owner:$owner,name:$name){
      refs(refPrefix:"refs/heads/",first:100,after:$endCursor){
        pageInfo{hasNextPage endCursor}
        nodes{name target{... on Commit{committedDate}}}
      }
    }
  }' --jq '.data.repository.refs.nodes[] | [.name, .target.committedDate] | @tsv')"

RELEASE_RE='^([0-9]+\.([0-9]+|x))$'
count=0
while IFS=$'\t' read -r branch date; do
  [[ -z "${branch}" || -z "${date}" ]] && continue
  [[ "${branch}" == "${DEFAULT_BRANCH}" ]] && continue
  grep -Fxq -- "${branch}" <<<"${PROTECTED_BRANCHES}" && continue
  [[ "${branch}" =~ ${RELEASE_RE} ]] && continue
  [[ ! "${date}" < "${CUTOFF}" ]] && continue
  # Only stale candidates are checked for open PRs, so there is no cap on the
  # number of open PRs in the repository. Fail safe: skip on any error.
  if ! open_prs="$(gh api --method GET "repos/${REPO}/pulls" \
    -f state=open -f head="${OWNER}:${branch}" -f per_page=1 --jq 'length')"; then
    echo "::warning::Could not check open PRs for ${branch}; skipping"
    continue
  fi
  [[ "${open_prs}" != "0" ]] && continue

  if [[ "${DRY_RUN}" == "true" ]]; then
    echo "[dry-run] would delete ${branch} (last commit ${date})"
  else
    echo "Deleting ${branch} (last commit ${date})"
    encoded="$(jq -rn --arg b "${branch}" '$b | @uri')"
    gh api -X DELETE "repos/${REPO}/git/refs/heads/${encoded}" >/dev/null \
      || { echo "::warning::Failed to delete ${branch}"; continue; }
  fi
  count=$((count + 1))
done <<<"${BRANCHES}"

echo "Stale branches $([[ "${DRY_RUN}" == "true" ]] && echo "found" || echo "deleted"): ${count}"
if [[ -n "${GITHUB_OUTPUT:-}" ]]; then
  echo "stale-branches-count=${count}" >> "${GITHUB_OUTPUT}"
fi
