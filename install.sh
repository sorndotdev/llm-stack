#!/usr/bin/env bash
# Symlinks skills and agents from this repo into Claude Code and OpenCode so they can use them.
# Idempotent: re-run after adding new skills/agents. Never overwrites real files/dirs.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
OPENCODE_DIR="$HOME/.config/opencode"

link() {
  local src="$1" dest="$2" err
  if [ -L "$dest" ]; then
    ln -sfn "$src" "$dest"
  elif [ -e "$dest" ]; then
    echo "skip: $dest exists and is not a symlink" >&2
    return
  elif ! err="$(ln -s "$src" "$dest" 2>&1)"; then
    echo "skip: cannot create $dest: $err" >&2
    return
  fi
  echo "linked: $dest -> $src"
}

install_into() {
  local config_dir="$1" skill agent

  mkdir -p "$config_dir/skills" "$config_dir/agents"

  for skill in "$REPO"/skills/*/; do
    skill="${skill%/}"
    link "$skill" "$config_dir/skills/$(basename "$skill")"
  done

  for agent in "$REPO"/agents/*.md; do
    link "$agent" "$config_dir/agents/$(basename "$agent")"
  done
}

clean_stale() {
  local config_dir="$1" dest

  # Remove dangling symlinks that point back into this repo (deleted/renamed items)
  for dest in "$config_dir"/skills/* "$config_dir"/agents/*; do
    if [ -L "$dest" ] && [ ! -e "$dest" ] && [[ "$(readlink "$dest")" == "$REPO"/* ]]; then
      rm "$dest"
      echo "removed stale: $dest"
    fi
  done
}

for config_dir in "$CLAUDE_DIR" "$OPENCODE_DIR"; do
  install_into "$config_dir"
  clean_stale "$config_dir"
done
