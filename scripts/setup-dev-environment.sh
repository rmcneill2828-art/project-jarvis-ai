#!/usr/bin/env bash
# Bootstraps a fresh clone of Project JARVIS AI for local development on macOS
# or Linux: installs npm and Rust dependencies, creates/updates the Python
# virtual environment, and activates the tracked pre-commit hook. Safe to
# re-run. The counterpart of setup-dev-environment.ps1 (ESR-0061 WP2b, EBG-0054).
#
#   scripts/setup-dev-environment.sh            set everything up
#   scripts/setup-dev-environment.sh --doctor   only report what is present or missing
#
# Prerequisites are installed by you (see scripts/PREREQUISITES.md); this script
# never installs system software, it only reports what is missing.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

doctor_only=0
case "${1:-}" in
  "") ;;
  --doctor) doctor_only=1 ;;
  -h | --help)
    sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit 0
    ;;
  *)
    echo "Unknown option: $1 (use --doctor or --help)" >&2
    exit 2
    ;;
esac

missing=0

# version_at_least ACTUAL MINIMUM: true when ACTUAL >= MINIMUM, comparing dotted
# numbers part by part. Plain bash arithmetic: `sort -V` is not on every
# macOS's sort, and macOS's bash is 3.2 (no associative arrays, no mapfile).
version_at_least() {
  local IFS=. i a m
  local -a actual minimum
  read -r -a actual <<< "$1"
  read -r -a minimum <<< "$2"
  for ((i = 0; i < ${#minimum[@]}; i++)); do
    a=${actual[i]:-0}
    m=${minimum[i]}
    if ((10#$a > 10#$m)); then return 0; fi
    if ((10#$a < 10#$m)); then return 1; fi
  done
  return 0
}

# check NAME COMMAND MIN_VERSION VERSION_COMMAND...
check() {
  local name="$1" cmd="$2" min="$3"
  shift 3
  if ! command -v "$cmd" > /dev/null 2>&1; then
    echo "  MISSING  $name ($cmd not found)"
    missing=1
    return
  fi
  if [ -z "$min" ]; then
    echo "  ok       $name"
    return
  fi
  local actual
  actual="$("$@" 2> /dev/null | grep -Eo '[0-9]+(\.[0-9]+)+' | head -n 1 || true)"
  if [ -z "$actual" ]; then
    echo "  ok       $name (version not detected; needs $min+)"
  elif version_at_least "$actual" "$min"; then
    echo "  ok       $name $actual"
  else
    echo "  TOO OLD  $name $actual (needs $min+)"
    missing=1
  fi
}

echo "==> Checking prerequisites..."
check "Git" git "" git --version
check "Node.js" node 18 node --version
check "npm" npm "" npm --version
check "Rust (cargo)" cargo "" cargo --version
check "Python" python3 3.12 python3 --version
if [ "$(uname -s)" = "Darwin" ]; then
  if xcode-select -p > /dev/null 2>&1; then
    echo "  ok       Xcode command line tools"
  else
    echo "  MISSING  Xcode command line tools (run: xcode-select --install)"
    missing=1
  fi
fi

if [ "$missing" -ne 0 ]; then
  echo "One or more prerequisites are missing. See scripts/PREREQUISITES.md, then re-run." >&2
  exit 1
fi

if [ "$doctor_only" -eq 1 ]; then
  echo "All prerequisites are present. (--doctor: nothing was changed.)"
  exit 0
fi

echo "==> Installing npm dependencies (from package-lock.json)..."
npm install

echo "==> Building the Rust/Tauri backend (first build compiles the full dependency tree)..."
(cd src-tauri && cargo build)

echo "==> Setting up the Python virtual environment (.venv)..."
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e ".[dev]"

echo "==> Activating the tracked pre-commit hook (git config core.hooksPath scripts/hooks)..."
git config core.hooksPath scripts/hooks

echo "==> Running repository validation and the test suite as a smoke test..."
.venv/bin/python scripts/validate_repository.py
.venv/bin/python -m pytest -q

echo
echo "Setup complete."
echo "Activate the Python environment in new shells with: source .venv/bin/activate"
