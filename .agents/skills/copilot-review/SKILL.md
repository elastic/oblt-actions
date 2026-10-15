---
name: copilot-review
description: Review pull requests in elastic/oblt-actions for concrete, high-impact defects using repository-specific checks.
---

# Copilot pull request review

Use this skill only when reviewing a pull request in `elastic/oblt-actions`. Follow the global review policies in `.github/instructions/review-policy-core.instructions.md`, `.github/instructions/review-policy-security.instructions.md`, and `.github/instructions/review-policy-tests.instructions.md`. Apply `.github/instructions/repository-review.instructions.md` and, for action or workflow changes, `.github/instructions/github-actions.instructions.md`.

## Review process

1. Read the complete pull request diff. For each possible finding, inspect only the relevant callers, configuration, tests, and documentation needed to verify it.
2. Report a finding only when the changed lines introduce or materially worsen a concrete failure. Confirm the repository supports the claim and describe a realistic trigger, mechanism, and user, security, reliability, or operational impact.
3. Prefer silence when impact or evidence is uncertain. Do not report wording, style, praise, speculative risks, unrelated existing defects, or diagnostics already enforced by CI and pre-commit.
4. Check meaningful existing coverage before requesting tests. When action behavior changes, look for the action's dedicated `.github/workflows/test-<action>.yml` or colocated tests; prefer end-to-end tests that invoke the composite action with `uses: ./<action-path>`.
5. Report concise, actionable findings tied to changed lines. Identify the failure and impact, then give the smallest corrective action or the specific evidence needed to verify safety.

## Repository-specific checks

- For `.github/workflows/trigger-obs-aw-*`, compare forwarded secret and environment names with the called `elastic/oblt-aw` reusable-workflow contract. Keep the trigger inventory in `README.md` aligned when mappings change; a name mismatch can make a downstream workflow run without the credential it requires.
- For `edot-release/**` or `.github/edot-release.json`, trace tag selection, full-history inputs, release-range output, version changes, and branch handoffs through preparation and finalization. A wrong boundary or handoff can publish an incorrect version or omit contributing pull requests.
- For `oblt-cli/deploy-my-kibana`, `oblt-cli/undeploy-my-kibana`, and their workflows, verify deploy and teardown issue labels remain aligned with the downstream handlers. Mismatched labels can lose a deployment request or leave an environment running after teardown.
- For `aws/auth`, `azure/auth`, and `google/auth`, check that account, project, tenant, and derived identity values refer to the intended cloud target. Incorrect mapping can authenticate to the wrong account or prevent cloud operations.
- When action metadata changes, check the declared inputs and outputs against callers and the action README. If the action's runtime behavior changes, verify the end-to-end test exercises the local action rather than only reimplementing its logic.

## Deterministic checks

Use the tool coverage listed in `.github/instructions/repository-review.instructions.md`. Do not repeat pre-commit, actionlint, action README generation, Jest, or Dependabot diagnostics in review comments. Focus on material behavior that those checks cannot establish.
