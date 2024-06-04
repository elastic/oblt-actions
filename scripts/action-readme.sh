#!/usr/bin/env bash

set -euo pipefail

find . \( -name "action.yml" -o -name "action.yaml" \) -exec dirname {} \; | while read -r dir; do
    printf "%s: " "$dir"
    gh action-readme update --action="$dir/action.yml" --readme="$dir/README.md"
done
