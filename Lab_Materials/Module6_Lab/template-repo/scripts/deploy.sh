#!/usr/bin/env bash
# SIMULATED deploy — prints what it would do. It never contacts a real environment.
# Safe to run in CI: it only echoes and exits 0.
set -euo pipefail

: "${DEPLOY_TOKEN:?DEPLOY_TOKEN must be supplied through the production environment secret}"

TARGET="unknown"
TRAFFIC="0"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)  TARGET="$2"; shift 2 ;;
    --traffic) TRAFFIC="$2"; shift 2 ;;
    *) shift ;;
  esac
done

echo "SIMULATED DEPLOY -> target=${TARGET} traffic=${TRAFFIC}%"
echo "(no real system is contacted; this is a lab)"
