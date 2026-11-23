# Release wizard helpers

These scripts provide the mechanical reads and workflow dispatches used by
EDOT SDK release wizard skills. They are scripts, rather than a GitHub Action;
each SDK keeps its own `SKILL.md` for release guidance and judgment.

| Script | Purpose |
|--------|---------|
| `repository.sh` | Read `repository` from `.github/edot-release.json` in the current directory. Sourced by the other scripts; fail with the file and field name when absent. |
| `release-state.sh` | Read release branches and pull requests from GitHub and print the phase and next operator actions as JSON. |
| `patch-preview.sh` | Resolve a patch line's source tag and next version with the shared `version.sh` at `v1`, then list cherry-pick candidates as JSON. Read `tagPrefix` from the current checkout's config. |
| `dispatch.sh` | Dispatch a release workflow with its ref and inputs, then wait for that exact run through `watch-run.sh`. |
| `watch-run.sh` | Follow an existing workflow run and report its outcome and URL. |
| `draft-notes.sh` | Dispatch Draft release notes and print the JSON from its `release-notes` artifact. |

Run the helpers from the SDK checkout root with Bash, `gh` authenticated for
that repository, `jq`, and Git available. Configure the GitHub repository as
`"repository": "owner/name"` in `.github/edot-release.json`. This field is
optional for the existing release actions and required by these helpers; see
[release configuration](../prepare-start/README.md#configuration).

The helpers never write repository files, merge pull requests, or create tags.
`patch-preview.sh` fetches existing tags into local Git metadata. Dispatches
start the existing release workflows; their release checks remain there.
Temporary scripts and downloaded artifacts live outside the checkout.

## Fetch at v1

A child's release wizard skill uses this Bash snippet to list and download all
shell scripts into a temporary directory, preserving their sibling layout.
Run it from the SDK checkout root, and retain `wizard_dir` for subsequent helper
calls in that session. Remove it with `rm -rf "$wizard_dir"` when finished.

```bash
set -euo pipefail
wizard_dir=$(mktemp -d)
if ! wizard_scripts=$(gh api \
  'repos/elastic/oblt-actions/contents/edot-release/wizard?ref=v1' \
  --jq '.[] | select(.type == "file" and (.name | endswith(".sh"))) | .name'); then
  rm -rf "$wizard_dir"
  exit 1
fi
while IFS= read -r script; do
  if ! gh api -H 'Accept: application/vnd.github.raw' \
    "repos/elastic/oblt-actions/contents/edot-release/wizard/$script?ref=v1" \
    > "$wizard_dir/$script"; then
    rm -rf "$wizard_dir"
    exit 1
  fi
  chmod +x "$wizard_dir/$script"
done <<< "$wizard_scripts"
```

For example, run `"$wizard_dir/release-state.sh"` to read the release phase.
Dispatch only after the operator confirms the proposed workflow and inputs.
If a dispatch's outcome is unknown, follow its reported run with
`"$wizard_dir/watch-run.sh" <run-id>` before dispatching again.
