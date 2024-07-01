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

input_version="${OBLT_CLI_VERSION:-}"
version_file="${OBLT_CLI_VERSION_FILE:-"${GITHUB_ACTION_PATH}/.default-oblt-cli-version"}"

if [[ -n "${version_file}" && -n "${input_version}" ]]; then
  echo "::warning title=elastic/oblt-actions/oblt-cli/setup::Both version and version-file are provided. Using version: ${input_version}."
fi

if [[ -n "${input_version}" ]]; then
  version="${OBLT_CLI_VERSION}"
else
  if [[ -f "${version_file}" ]]; then
    case $(basename "$version_file") in
    ".tool-versions")
      version=$(grep "^oblt-cli" "${version_file}" | awk '{ printf $2 }')
      ;;
    *)
      version=$(tr -d '[:space:]' <"${version_file}")
      ;;
    esac
  else
    echo "::error title=elastic/oblt-actions/oblt-cli/setup::version-file not found: ${version_file}"
    exit 1
  fi
fi

gh release download "${version}" \
  --skip-existing \
  --repo elastic/observability-test-environments \
  -p "${PATTERN}" \
  --output - | tar -xz -C "${BIN_DIR}"
echo "::notice title=elastic/oblt-actions/oblt-cli/setup::Downloaded oblt-cli version: ${version}"
echo "${BIN_DIR}" >> "${GITHUB_PATH}"
