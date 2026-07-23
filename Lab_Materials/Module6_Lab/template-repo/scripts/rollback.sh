#!/usr/bin/env bash
# SIMULATED rollback — prints what it would do. Never contacts a real environment.
set -euo pipefail
echo "SIMULATED ROLLBACK -> reverting to previous release"
echo "(no real system is contacted; this is a lab)"
