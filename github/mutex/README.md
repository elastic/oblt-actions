# mutex

A simple locking/unlocking mechanism to provide mutual exclusion in GitHub Actions.

## Getting Started

To prevent concurrent access to a job:

```yaml
jobs:
  run_in_mutex:
    runs-on: ubuntu-latest
    name: Simple mutex test
    steps:
      - uses: actions/checkout@v4
      - name: Set up mutex
        uses: elastic/oblt-actions/mutex@main
      - run: |
          echo "I am protected!"
          sleep 5
```

By default, the `mutex` branch in the current repo is used to store the state of locks.

To have multiple mutexes, specify the `branch` input:

```yaml
jobs:
  two_clients_test_client_1:
    runs-on: ubuntu-latest
    name: Two clients test (client 1)
    steps:
      - uses: actions/checkout@v4
      - name: Set up mutex
        uses: elastic/oblt-actions/mutex@main
        with:
          branch: another-mutex
      - run: |
          echo "I am protected by the 'another-mutex' mutex!"
          sleep 5
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `github-token` | The token for accessing the repo. | No | `${{ github.token }}` |

| `repository` | The repository path that stores the lock. | No | `${{ github.repository }}` |
| `branch` | The branch to use for the mutex. | No | `mutex` |
| `suffix` | Suffix to avoid identical values for parallel/matrix jobs in the same workflow run. | No | `default` |
| `timeout-minutes` | Maximum wait time for acquiring the lock in minutes. | No | `30` |

## Advanced Usage

### Using a different repository for the mutex

You can store the mutex state in a different repository. This allows sharing a mutex between jobs from arbitrary repos:

```yaml
- name: Set up mutex
  uses: elastic/oblt-actions/mutex@main
  with:
    github-token: ${{ secrets.PAT_TOKEN }}
    repository: my-org/shared-mutex-repo
```

### Parallel/matrix jobs

When running parallel or matrix jobs, use `suffix` to ensure each job gets a unique ticket:

```yaml
strategy:
  matrix:
    env: [staging, production]
steps:
  - uses: actions/checkout@v4
  - name: Set up mutex
    uses: elastic/oblt-actions/mutex@main
    with:
      suffix: ${{ matrix.env }}
```

### Timeout configuration

By default, the action will wait up to 30 minutes to acquire the lock. You can customize this timeout using the `timeout-minutes` input:

```yaml
- name: Set up mutex with custom timeout
  uses: elastic/oblt-actions/mutex@main
  with:
    timeout-minutes: 60
```

## Developing

### Prerequisites

- [Node.js](https://nodejs.org/) (v20 or later)

### Building

```bash
npm install
npm run build
```

The `npm run build` command uses `@vercel/ncc` to compile the source files into self-contained bundles in `dist/lock/` and `dist/unlock/`.

### Testing locally

1. Install [act](https://github.com/nektos/act).
2. Populate `.github-token` with a personal access token with the `repo` permission.
3. `act --rebuild -v -s GITHUB_TOKEN=$(cat .github-token)`
