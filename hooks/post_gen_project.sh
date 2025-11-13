#!/usr/bin/env bash
set -o errexit
set -o pipefail

echo "[cookiecutter] Initializing git repository..."
if ! command -v git >/dev/null 2>&1; then
  echo "[cookiecutter] git not available, skipping repo initialization."
  exit 0
fi

if git rev-parse --git-dir >/dev/null 2>&1; then
  echo "[cookiecutter] Repository already initialized, skipping."
  exit 0
fi

git init
git branch -m main
git add .
git commit -m "chore: bootstrap {{cookiecutter.project_name}}"

REMOTE_URL="{{cookiecutter.git_remote}}"
git remote add origin "${REMOTE_URL}"
echo "[cookiecutter] Git remote set to ${REMOTE_URL}"
