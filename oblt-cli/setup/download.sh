#!/usr/bin/env bash

set -euo pipefail

BIN_DIR="$HOME/oblt-cli/bin"

mkdir -p "${BIN_DIR}"

if [[ ${RUNNER_OS} == "Linux" ]]; then
  if [[ ${RUNNER_ARCH} == "X64" ]]; then
    PATTERN='*linux_amd64.tar.gz'
  elif [[ ${RUNNER_ARCH} == "ARM64" ]]; then
    PATTERN='*linux_arm64.tar.gz'
  else
    echo "Unsupported architecture for ${RUNNER_OS}: ${RUNNER_ARCH}"
    exit 1
  fi
elif [[ ${RUNNER_OS} == "macOS" ]]; then
  if [[ ${RUNNER_ARCH} == "X64" ]]; then
      PATTERN='*darwin_amd64.tar.gz'
    elif [[ ${RUNNER_ARCH} == "ARM64" ]]; then
      PATTERN='*darwin_arm64.tar.gz'
    else
      echo "Unsupported architecture for ${RUNNER_OS}: ${RUNNER_ARCH}"
      exit 1
    fi
else
  echo "Unsupported OS: ${RUNNER_OS}"
  exit 1
fi

# Downloads the latest release if OBLT_CLI_VERSION is not set
gh release download "${OBLT_CLI_VERSION}" \
  --repo elastic/observability-test-environments \
  -p "${PATTERN}" \
  --output - | tar -xz -C "${BIN_DIR}"

echo "${BIN_DIR}" >> "${GITHUB_PATH}"
