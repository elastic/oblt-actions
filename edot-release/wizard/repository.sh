#!/usr/bin/env bash
#
# Read the release wizard's GitHub repository from the current checkout's
# config, so every helper dispatches and reads the same repository.
# Sourced by the other helpers; it prints nothing on success.

config_file=.github/edot-release.json
# shellcheck disable=SC2034
if ! repository=$(jq -er '.repository | select(type == "string" and length > 0)' "$config_file" 2>/dev/null); then
  echo "$config_file: repository must name the GitHub repository (owner/name)." >&2
  exit 1
fi
