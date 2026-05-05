#!/bin/bash
set -e

# --- Configuration ---
GLOBAL_MEMORY="${HOME}/.gemini/antigravity/memory"
PROJECT_MEMORY="${PWD}/.agents/memory"
# The repository to backup to (can be configured by the user)
REPO_DIR="${GLOBAL_MEMORY}/.git-repo"

if [ ! -d "${REPO_DIR}/.git" ]; then
  echo "[backup] Backup repo not found: ${REPO_DIR}"
  echo "[backup] Please initialize it: mkdir -p ${REPO_DIR} && cd ${REPO_DIR} && git init"
  exit 1
fi

do_pull() {
  cd "${REPO_DIR}"
  git pull --quiet origin main 2>/dev/null || git pull origin main 2>/dev/null || true
  echo "[backup] Pulled latest from GitHub"

  # Distribute to global memory
  mkdir -p "${GLOBAL_MEMORY}"
  for f in "${REPO_DIR}/global/"*.md; do
    [ -f "${f}" ] || continue
    basename_f=$(basename "${f}")
    if [ ! -f "${GLOBAL_MEMORY}/${basename_f}" ] || [ "${f}" -nt "${GLOBAL_MEMORY}/${basename_f}" ]; then
      cp "${f}" "${GLOBAL_MEMORY}/${basename_f}"
    fi
  done

  # Distribute to project memory
  mkdir -p "${PROJECT_MEMORY}"
  proj_name=$(basename "${PWD}")
  if [ -d "${REPO_DIR}/projects/${proj_name}" ]; then
    for f in "${REPO_DIR}/projects/${proj_name}/"*.md; do
      [ -f "${f}" ] || continue
      basename_f=$(basename "${f}")
      if [ ! -f "${PROJECT_MEMORY}/${basename_f}" ] || [ "${f}" -nt "${PROJECT_MEMORY}/${basename_f}" ]; then
        cp "${f}" "${PROJECT_MEMORY}/${basename_f}"
      fi
    done
  fi
}

do_push_local() {
  mkdir -p "${REPO_DIR}/global"
  if [ -d "${GLOBAL_MEMORY}" ]; then
    for f in "${GLOBAL_MEMORY}/"*.md; do
      [ -f "${f}" ] || continue
      basename_f=$(basename "${f}")
      cp "${f}" "${REPO_DIR}/global/${basename_f}"
    done
  fi

  proj_name=$(basename "${PWD}")
  mkdir -p "${REPO_DIR}/projects/${proj_name}"
  if [ -d "${PROJECT_MEMORY}" ]; then
    for f in "${PROJECT_MEMORY}/"*.md; do
      [ -f "${f}" ] || continue
      basename_f=$(basename "${f}")
      cp "${f}" "${REPO_DIR}/projects/${proj_name}/${basename_f}"
    done
  fi
}

do_commit() {
  cd "${REPO_DIR}"
  git add -A
  if git diff --cached --quiet; then
    echo "[backup] Nothing to commit"
    return 1
  fi
  DATE=$(date +%Y-%m-%d)
  TIME=$(date +%H:%M)
  CHANGED=$(git diff --cached --name-only | head -10 | tr '\n' ', ' | sed 's/,$//')
  git commit -m "backup ${DATE} ${TIME}: ${CHANGED}" --quiet
  echo "[backup] Committed: ${CHANGED}"
  return 0
}

do_git_push() {
  cd "${REPO_DIR}"
  git push --quiet 2>/dev/null || true
  echo "[backup] Pushed to GitHub"
}

case "$1" in
  pull)
    do_pull
    ;;
  sync)
    do_pull
    do_push_local
    do_commit && do_git_push
    ;;
  push)
    do_push_local
    do_commit && do_git_push
    ;;
  *)
    do_push_local
    do_commit || true
    ;;
esac
