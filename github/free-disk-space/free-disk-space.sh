#!/usr/bin/env bash
# Copied from https://github.com/lumbroso-commons/free-disk-space
# at v2.0.0 (ceedf095f4ec1a097402bc6bd80831f2e1a6fde6), the `run` block of its action.yml.
# Copyright (c) 2022 Jérémie Lumbroso. MIT License, see LICENSE in this directory.
# Only the indentation differs from upstream.

# ======
# MACROS
# ======

# macro to print a line of equals
# (silly but works)
printSeparationLine() {
  str=${1:=}
  num=${2:-80}
  counter=1
  output=""
  while [ $counter -le $num ]
  do
     output="${output}${str}"
     counter=$((counter+1))
  done
  echo "${output}"
}

# macro to compute available space
# REF: https://unix.stackexchange.com/a/42049/60849
# REF: https://stackoverflow.com/a/450821/408734
getAvailableSpace() { echo $(df -a $1 | awk 'NR > 1 {avail+=$4} END {print avail}'); }

# macro to make Kb human readable (assume the input is Kb)
# REF: https://unix.stackexchange.com/a/44087/60849
formatByteCount() { echo $(numfmt --to=iec-i --suffix=B --padding=7 $1'000'); }

# macro to output saved space
printSavedSpace() {
  saved=${1}
  title=${2:-}

  echo ""
  printSeparationLine '*' 80
  if [ ! -z "${title}" ]; then
    echo "=> ${title}: Saved $(formatByteCount $saved)"
  else
    echo "=> Saved $(formatByteCount $saved)"
  fi
  printSeparationLine '*' 80
  echo ""
}

# macro to print output of dh with caption
printDH() {
  caption=${1:-}

  printSeparationLine '=' 80
  echo "${caption}"
  echo ""
  echo "$ dh -h /"
  echo ""
  df -h /
  echo "$ dh -a /"
  echo ""
  df -a /
  echo "$ dh -a"
  echo ""
  df -a
  printSeparationLine '=' 80
}



# ======
# SCRIPT
# ======

# Display initial disk space stats

AVAILABLE_INITIAL=$(getAvailableSpace)
AVAILABLE_ROOT_INITIAL=$(getAvailableSpace '/')

printDH "BEFORE CLEAN-UP:"
echo ""


# Option: Remove Android library

if [[ "$ANDROID" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  sudo rm -rf /usr/local/lib/android || true

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Android library"
fi

# Option: Remove .NET runtime

if [[ "$DOTNET" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  # https://github.community/t/bigger-github-hosted-runners-disk-space/17267/11
  sudo rm -rf /usr/share/dotnet || true

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED ".NET runtime"
fi

# Option: Remove Haskell runtime

if [[ "$HASKELL" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  sudo rm -rf /opt/ghc || true
  sudo rm -rf /usr/local/.ghcup || true

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Haskell runtime"
fi

# Option: Remove large packages
# REF: https://github.com/apache/flink/blob/master/tools/azure-pipelines/free_disk_space.sh

if [[ "$LARGE_PACKAGES" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  # PRECEDENCE: a specific subject-toggle outranks this general category.
  # Setting `dotnet: false` keeps .NET everywhere, including the apt
  # packages this block would otherwise sweep up.
  #
  # Reported by @gmij in #6 (2023), again by @ashleney in #33 (2024), and
  # diagnosed with a workaround by @ax3l in #33 (2025).
  #
  # The policy is explicit; this applies it to .NET. A future subject
  # option must add and test its own exemption here — there is no general
  # mechanism that does it automatically.
  if [[ "$DOTNET" == 'true' ]]; then
    sudo apt-get remove -y '^aspnetcore-.*' || echo "::warning::The command [sudo apt-get remove -y '^aspnetcore-.*'] failed to complete successfully. Proceeding..."
    sudo apt-get remove -y '^dotnet-.*' --fix-missing || echo "::warning::The command [sudo apt-get remove -y '^dotnet-.*' --fix-missing] failed to complete successfully. Proceeding..."
  else
    echo "::notice::dotnet: false — .NET packages exempted from large-packages (dotnet-*, aspnetcore-*)."
  fi

  sudo apt-get remove -y '^llvm-.*' --fix-missing || echo "::warning::The command [sudo apt-get remove -y '^llvm-.*' --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y 'php.*' --fix-missing || echo "::warning::The command [sudo apt-get remove -y 'php.*' --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y '^mongodb-.*' --fix-missing || echo "::warning::The command [sudo apt-get remove -y '^mongodb-.*' --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y '^mysql-.*' --fix-missing || echo "::warning::The command [sudo apt-get remove -y '^mysql-.*' --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y azure-cli google-chrome-stable firefox powershell mono-devel libgl1-mesa-dri --fix-missing || echo "::warning::The command [sudo apt-get remove -y azure-cli google-chrome-stable firefox powershell mono-devel libgl1-mesa-dri --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y google-cloud-sdk --fix-missing || echo "::debug::The command [sudo apt-get remove -y google-cloud-sdk --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get remove -y google-cloud-cli --fix-missing || echo "::debug::The command [sudo apt-get remove -y google-cloud-cli --fix-missing] failed to complete successfully. Proceeding..."
  sudo apt-get autoremove -y || echo "::warning::The command [sudo apt-get autoremove -y] failed to complete successfully. Proceeding..."
  sudo apt-get clean || echo "::warning::The command [sudo apt-get clean] failed to complete successfully. Proceeding..."

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Large misc. packages"
fi

# Option: Remove Docker images

if [[ "$DOCKER_IMAGES" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  sudo docker image prune --all --force || true

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Docker images"
fi

# Option: Remove tool cache
# REF: https://github.com/actions/virtual-environments/issues/2875#issuecomment-1163392159

# `tool-cache` was renamed `preinstalled-runtimes` in v2.0.0. The old
# input is still honoured so no existing workflow breaks; either one
# being true removes the directory. The warning fires only when someone
# actually relies on the old name — an expected-absence stays quiet,
# per the severity convention in docs/adr/0004.
if [[ "$TOOL_CACHE" == 'true' ]]; then
  echo "::warning::The 'tool-cache' input is deprecated; it was renamed to 'preinstalled-runtimes'. It still works and will keep working until v3.0.0 — please rename it when convenient."
fi

if [[ "$PREINSTALLED_RUNTIMES" == 'true' || "$TOOL_CACHE" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  sudo rm -rf "$AGENT_TOOLSDIRECTORY" || true

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Pre-installed runtimes"
fi

# Option: Remove Swap storage

if [[ "$SWAP_STORAGE" == 'true' ]]; then
  BEFORE=$(getAvailableSpace)

  sudo swapoff -a || true
  sudo rm -f /mnt/swapfile || true
  free -h

  AFTER=$(getAvailableSpace)
  SAVED=$((AFTER-BEFORE))
  printSavedSpace $SAVED "Swap storage"
fi



# Output saved space statistic

AVAILABLE_END=$(getAvailableSpace)
AVAILABLE_ROOT_END=$(getAvailableSpace '/')

echo ""
printDH "AFTER CLEAN-UP:"

echo ""
echo ""

echo "/dev/root:"
printSavedSpace $((AVAILABLE_ROOT_END - AVAILABLE_ROOT_INITIAL))
echo "overall:"
printSavedSpace $((AVAILABLE_END - AVAILABLE_INITIAL))
