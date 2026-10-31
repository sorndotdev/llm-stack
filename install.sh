#!/usr/bin/env bash
# Symlinks skills and agents from this repo into Claude Code and OpenCode so they can use them.
# Hooks go to Claude Code only.
# Idempotent: re-run after adding new skills/agents/hooks. Never overwrites real files/dirs,
# except hook copies identical to the repo's (replaced by symlinks) and settings.json,
# whose env block is overlaid from claude/settings.json.
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

# Overlay the repo's env keys onto Claude Code's settings.json. Other keys stay local.
merge_settings() {
  local config_dir="$1" src="$REPO/claude/settings.json" dest="$config_dir/settings.json" tmp

  [ -f "$src" ] || return 0

  if ! command -v jq >/dev/null; then
    echo "skip: jq not installed, cannot merge $src" >&2
    return
  fi

  if [ ! -e "$dest" ]; then
    cp "$src" "$dest"
    echo "created: $dest"
    return
  fi

  tmp="$(mktemp)"
  if ! jq --slurpfile overlay "$src" '
    .env = ((.env // {}) + ($overlay[0].env // {}))
    | reduce ($overlay[0] | to_entries[] | select(.key != "env")) as $e (. ; .[$e.key] = $e.value)
  ' "$dest" >"$tmp"; then
    rm -f "$tmp"
    echo "skip: cannot merge $src into $dest" >&2
    return
  fi
  if cmp -s "$tmp" "$dest"; then
    rm -f "$tmp"
    return
  fi
  mv "$tmp" "$dest"
  echo "merged: $src -> $dest"
}

install_into() {
  local config_dir="$1" skill agent hook

  mkdir -p "$config_dir/skills" "$config_dir/agents"

  for skill in "$REPO"/skills/*/; do
    skill="${skill%/}"
    link "$skill" "$config_dir/skills/$(basename "$skill")"
  done

  for agent in "$REPO"/agents/*.md; do
    # Claude Code reads main-session instructions from CLAUDE.md; OpenCode reads them as an agent.
    if [ "$(basename "$agent")" = global.md ] && [ "$config_dir" = "$CLAUDE_DIR" ]; then
      link "$agent" "$config_dir/CLAUDE.md"
    else
      link "$agent" "$config_dir/agents/$(basename "$agent")"
    fi
  done

  # Settings and hooks are Claude Code only.
  if [ "$config_dir" = "$CLAUDE_DIR" ]; then
    merge_settings "$config_dir"
    mkdir -p "$config_dir/hooks"
    for hook in "$REPO"/hooks/*; do
      # Replace a real copy identical to the repo's so it becomes a symlink; a differing one stays.
      if [ -f "$config_dir/hooks/$(basename "$hook")" ] && [ ! -L "$config_dir/hooks/$(basename "$hook")" ] \
        && cmp -s "$hook" "$config_dir/hooks/$(basename "$hook")"; then
        rm "$config_dir/hooks/$(basename "$hook")"
      fi
      link "$hook" "$config_dir/hooks/$(basename "$hook")"
    done
  fi
}

clean_stale() {
  local config_dir="$1" dest

  # Remove dangling symlinks that point back into this repo (deleted/renamed items)
  for dest in "$config_dir"/skills/* "$config_dir"/agents/* "$config_dir"/hooks/*; do
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
