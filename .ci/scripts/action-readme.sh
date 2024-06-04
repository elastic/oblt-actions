#!/usr/bin/env bash

# This script updates the README.md files in the directories that contain both an action.yml and a README.md file.
# Prerequisites:
# - gh: GitHub CLI
#
set -euo pipefail

function find_dirs_with_action_yml_and_readme_md() {
    find . \( -name 'action.yml' -o -name 'README.md' \) -exec dirname {} \; \
    | sort \
    | uniq -c \
    | grep -E '^\s+2' \
    | awk '{ print $2 }'
}

for dir in $(find_dirs_with_action_yml_and_readme_md); do
  gh action-readme update --action="$dir/action.yml" --readme="$dir/README.md"
done
