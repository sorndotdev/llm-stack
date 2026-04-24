#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
UPDATE=0

usage() {
  cat <<'EOF'
Usage: ./install.sh [--update]

Install skills and agents into the global Claude and OpenCode directories.
Unrelated entries are left untouched.

  --update   Overwrite entries that already exist.
  -h, --help Show this help.
EOF
}

for arg in "$@"; do
  case "$arg" in
    --update)
      UPDATE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'unknown option: %s\n' "$arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

install_items() {
  local src_dir="$1"
  local dest_dir="$2"
  local label="$3"
  local src name dest

  if [ -L "$dest_dir" ]; then
    printf 'skip %s: %s is a symlink\n' "$label" "$dest_dir" >&2
    return 0
  fi

  mkdir -p "$dest_dir"

  for src in "$src_dir"/*; do
    [ -e "$src" ] || continue

    name="$(basename "$src")"
    dest="$dest_dir/$name"

    if { [ -e "$dest" ] || [ -L "$dest" ]; } && [ "$UPDATE" -eq 0 ]; then
      printf 'skip %s (exists): %s\n' "$label" "$dest"
      continue
    fi

    rm -rf "$dest"
    cp -R "$src" "$dest"
    printf 'installed %s: %s\n' "$label" "$dest"
  done
}

install_items "$ROOT/skills" "$HOME/.claude/skills" skill
install_items "$ROOT/agents" "$HOME/.claude/agents" agent
install_items "$ROOT/skills" "$HOME/.config/opencode/skills" skill
install_items "$ROOT/agents" "$HOME/.config/opencode/agents" agent
