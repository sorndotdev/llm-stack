#!/usr/bin/env bash
# Symlinks skills and agents from this repo into ~/.claude so Claude Code can use them.
# Idempotent: re-run after adding new skills/agents. Never overwrites real files/dirs.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

link() {
  local src="$1" dest="$2"
  if [ -L "$dest" ]; then
    ln -sfn "$src" "$dest"
  elif [ -e "$dest" ]; then
    echo "skip: $dest exists and is not a symlink" >&2
    return
  else
    ln -s "$src" "$dest"
  fi
  echo "linked: $dest -> $src"
}

mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

for skill in "$REPO"/skills/*/; do
  skill="${skill%/}"
  link "$skill" "$CLAUDE_DIR/skills/$(basename "$skill")"
done

for agent in "$REPO"/agents/*.md; do
  link "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
done

# Remove dangling symlinks that point back into this repo (deleted/renamed items)
for dest in "$CLAUDE_DIR"/skills/* "$CLAUDE_DIR"/agents/*; do
  if [ -L "$dest" ] && [ ! -e "$dest" ] && [[ "$(readlink "$dest")" == "$REPO"/* ]]; then
    rm "$dest"
    echo "removed stale: $dest"
  fi
done
