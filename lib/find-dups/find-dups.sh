#!/bin/bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")"; pwd)"

# various file and directory paths
tooldir="$HERE/"duplicate-code-detection-tool
venvdir="$HERE/"venv
python="$venvdir/bin/python3"
pip="$venvdir/bin/pip"
requirements="$HERE/"requirements.txt

set -x

if ! [ -d "$tooldir/.git" ]; then
  git clone https://github.com/platisd/duplicate-code-detection-tool.git "$tooldir"
fi
if ! [ -d "$venvdir" ] || [ "$requirements" -nt "$venvdir" ]; then
  rm -rf "$venvdir"
  python3 -m venv "$venvdir"
  "$pip" install -r "$requirements"
  touch "$venvdir"
fi

# shellcheck disable=SC2046  # "quote to prevent word splitting"
"$python" \
    -W ignore \
    "$tooldir/duplicate_code_detection.py" \
    -f $(
        git ls-files "$@" |
        exists -f
    ) \
    --json - |
  jq \
  --arg pwd "$PWD" \
  -f "$HERE/"find-dups.jq \
;
