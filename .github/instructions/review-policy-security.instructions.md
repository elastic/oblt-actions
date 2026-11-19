---
applyTo: "**"
---

## Trust-boundary and supply-chain changes

Always inspect a diff that changes CI, build, release, dependency, credential,
network, or security configuration. Note: Copilot code review does not inspect
lockfiles, `requirements.txt`, or generated files — leave those to Dependabot
and human review. Leave a review comment when the change introduces or materially
broadens a capability without a concrete, repository-supported need and an
appropriate control. In particular, flag:

- broader token, role, cloud, repository, or secret permissions than the changed
  operation requires;
- new collection, copying, logging, caching, artifact upload, or persistence of
  credentials or secret-bearing worker state;
- privileged workflows that check out, download, or execute untrusted pull-
  request code, artifacts, build scripts, hooks, or dependency lifecycle scripts;
- new outbound destinations, telemetry, uploads, remote shells, or network
  services unrelated to the repository's documented responsibility;
- downloaded or remotely referenced code, actions, reusable workflows, images,
  plugins, tools, or binaries that are executed without immutable identity and
  integrity verification;
- new dependencies or build inputs that are not resolved immutably;
- weakened or bypassed tests, approval gates, secret scanning, signature or
  checksum verification, TLS verification, sandboxing, or least-privilege
  defaults;
- shared caches, workspaces, or non-ephemeral runners that allow an untrusted or
  earlier build to influence a privileged or later build;
- unexplained executable binaries, encoded or obfuscated payloads, generated
  code without a documented generator, or functionality unrelated to the
  repository's stated purpose;
- untrusted input, such as a pull-request title, branch name, or issue body,
  placed directly into a `run:` script through a `${{ }}` expression instead
  of through an environment variable.

For GitHub Actions, require third-party actions and reusable workflows to be
pinned to a full commit SHA from the intended upstream repository. Require
container images by digest when they execute in CI, build, release, or
production paths. Require downloaded executables or scripts to be pinned to an
immutable version and verified before execution with an expected cryptographic
digest, or with a signature or attestation from an expected signer. HTTPS or a
checksum downloaded from the same mutable source is not sufficient integrity
evidence. Reject pipe-to-shell execution of unverified remote content.

For package-manager dependencies, require the repository's lockfile or equivalent
immutable resolution to be committed and enforced. Do not comment on a version
range merely because it is a range when an enforced lockfile pins the resolved
artifact. Do comment when a new executable build or runtime dependency can float
without reviewed immutable resolution.

Describe the exact new trust path, the realistic abuse or compromise scenario,
and the smallest corrective control. Do not allege malicious intent; when code
appears unrelated or concealed, ask for concrete purpose and provenance and
recommend removal when neither is established.
