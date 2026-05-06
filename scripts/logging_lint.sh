#!/usr/bin/env bash
set -euo pipefail
if rg -n "print\(" backend libs | rg -v "tests"; then
  echo "print() found in non-test code"
  exit 1
fi
