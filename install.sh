#!/usr/bin/env bash
# Symlinks skills, agents, and hooks from this repo into Claude Code so it can use them.
# Idempotent: re-run after adding new skills/agents/hooks. Never overwrites real files/dirs,
# except hook copies identical to the repo's (replaced by symlinks) and settings.json,
# whose env and hooks are merged from claude/settings.json.
set -euo pipefail

REPO="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

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

# Overlay the repo's env keys onto Claude Code's settings.json and merge hooks per event.
# Other keys override local ones.
merge_settings() {
  local config_dir="$1" src="$REPO/claude/settings.json" tmp
  local dest="$config_dir/settings.json"

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
    | reduce ($overlay[0] | to_entries[] | select(.key != "env")) as $e (.;
        if $e.key == "hooks" and (.hooks | type) == "object" and ($e.value | type) == "object" then
          .hooks = (reduce ($e.value | to_entries[]) as $h (.hooks;
            .[$h.key] = (((.[$h.key] // []) + $h.value) | unique_by(tojson))))
        else
          .[$e.key] = $e.value
        end)
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
  local skill agent hook

  mkdir -p "$CLAUDE_DIR/skills" "$CLAUDE_DIR/agents"

  for skill in "$REPO"/skills/*/; do
    skill="${skill%/}"
    link "$skill" "$CLAUDE_DIR/skills/$(basename "$skill")"
  done

  for agent in "$REPO"/agents/*.md; do
    # Claude Code reads main-session instructions from CLAUDE.md.
    if [ "$(basename "$agent")" = global.md ]; then
      link "$agent" "$CLAUDE_DIR/CLAUDE.md"
    else
      link "$agent" "$CLAUDE_DIR/agents/$(basename "$agent")"
    fi
  done

  merge_settings "$CLAUDE_DIR"
  mkdir -p "$CLAUDE_DIR/hooks"
  for hook in "$REPO"/hooks/*; do
    # Replace a real copy identical to the repo's so it becomes a symlink; a differing one stays.
    if [ -f "$CLAUDE_DIR/hooks/$(basename "$hook")" ] && [ ! -L "$CLAUDE_DIR/hooks/$(basename "$hook")" ] \
      && cmp -s "$hook" "$CLAUDE_DIR/hooks/$(basename "$hook")"; then
      rm "$CLAUDE_DIR/hooks/$(basename "$hook")"
    fi
    link "$hook" "$CLAUDE_DIR/hooks/$(basename "$hook")"
  done
}

clean_stale() {
  local dest

  # Remove dangling symlinks that point back into this repo (deleted/renamed items)
  for dest in "$CLAUDE_DIR"/skills/* "$CLAUDE_DIR"/agents/* "$CLAUDE_DIR"/hooks/*; do
    if [ -L "$dest" ] && [ ! -e "$dest" ] && [[ "$(readlink "$dest")" == "$REPO"/* ]]; then
      rm "$dest"
      echo "removed stale: $dest"
    fi
  done
}

install_into
clean_stale
