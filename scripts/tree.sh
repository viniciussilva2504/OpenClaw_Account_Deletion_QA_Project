#!/usr/bin/env bash
set -euo pipefail
find . -maxdepth 3 -type f \\
  ! -path './.git/*' \\
  | sort
