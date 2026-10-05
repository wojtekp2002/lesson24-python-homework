#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist
{
  echo "Build report"
  echo "Repository: ${GITHUB_REPOSITORY:-local}"
  echo "Branch: ${GITHUB_REF_NAME:-local}"
  echo "Commit: ${GITHUB_SHA:-local}"
  echo "Python: $(python --version 2>&1)"
  echo "Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > dist/build-report.txt

python -m compileall -q src
echo "Build completed successfully."
