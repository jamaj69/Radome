#!/usr/bin/env bash
set -euo pipefail

# Compatibilidade apenas: nenhuma base é manipulada neste wrapper.
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec /home/python/pyenv/bin/python "${SCRIPT_DIR}/run_pipeline.py" "$@"
