---
applyTo: ".github/workflows/**, **/action.yml, **/*.sh, **/*.py, **/*.js, **/*.ts"
---

# GitHub Actions guidance

- Review workflow triggers, job dependencies, conditions, and reusable-workflow calls together; incorrect routing can skip tests or run an action in an unintended context.
- Keep workflow and job `permissions` least-privilege. For OIDC or token changes, verify the trust conditions and scope; excess access can enable unintended cloud operations or repository writes.
- Use explicit token scoping and OIDC where appropriate. Do not log or expose secrets, and validate untrusted input before passing it to shell commands.
- For workflow and composite-action changes, verify actual behavior with the corresponding test workflow, exercising the action via `uses: ./<action-path>`.
- Keep actions focused on one job and preserve their documented input/output contracts for callers.
- When action inputs, outputs, or usage change, update the corresponding README and keep examples consistent with `action.yml`.
