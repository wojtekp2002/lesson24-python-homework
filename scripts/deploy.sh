#!/usr/bin/env bash
set -euo pipefail

mkdir -p dist
{
  echo "Deployment report"
  echo "Environment: ${APP_ENV:-production}"
  echo "Application: ${APP_NAME:-lesson25-ci-cd}"
  echo "Branch: ${GITHUB_REF_NAME:-local}"
  echo "Commit: ${GITHUB_SHA:-local}"
  echo "Deployment mode: simulated production deployment"
  echo "Generated at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > dist/deploy-report.txt

echo "Simulated production deployment completed."
