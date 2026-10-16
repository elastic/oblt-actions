---
applyTo: "**"
---

# High-signal code review policy

These rules apply only when reviewing a pull request. They do not apply to Copilot Chat or cloud agent tasks. When reviewing, default to leaving no comment. Comment only when the changed code introduces a concrete correctness, security, data-integrity, compatibility, reliability, rollout, or operability defect, or when changed material behavior has no test that would catch a regression (see "Missing tests for material behavior" below).

When multiple issues compete for attention, prioritize in this order: (1) concrete correctness, security, or data-integrity defects; (2) architectural or design problems with a concrete, describable consequence; (3) missing test coverage for changed behavior. Leave the highest-priority comments first.

Do not comment on wording, spelling, formatting, naming preferences, syntax, style, import ordering, or other concerns that a compiler, formatter, linter, schema validator, test, or CI check enabled in this repository already reports. Do not restate a failing automated check. Do not leave praise, summaries, optional refactors, generic best practices, or speculative suggestions.

Before leaving a comment, verify all of the following:

- The issue is introduced or made materially worse by this pull request.
- You can describe a specific failure scenario and its impact.
- The finding starts from the changed lines. You may read callers, tests, and configuration to confirm it, but do not report issues the diff does not introduce or make worse.
- The repository's current code and configuration support the claim.
- The comment identifies the affected path and gives an actionable correction or asks for concrete missing evidence.
- The expected value of the comment is high enough to interrupt a human reviewer.

If any condition is missing, remain silent. Express uncertainty only when the uncertainty itself is a material risk that the author can resolve with specific evidence. On a re-review after new commits, do not repeat a comment on a line that has not changed since the prior run.

Use the repository's `.github/skills/code-review/SKILL.md` for domain-specific review checks when it exists. Copilot review is advisory. Whether its approval counts toward required approvals is controlled by org and branch settings, not this file.
