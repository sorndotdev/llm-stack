Personal workspace of custom skills, agents, and API scripts

## Install

Run `./install.sh` to symlink `skills/*` and `agents/*.md` into `~/.claude/`. `agents/global.md` installs as `~/.claude/CLAUDE.md`. `hooks/*` link into `~/.claude/hooks/` only; identical copies there are replaced by symlinks. Keys in `claude/settings.json` are merged into `~/.claude/settings.json`: `env` keys merge individually, `hooks` merge per event with identical entries deduplicated, and other keys override. Settings absent from that file, including the auth token, stay local. Re-run after adding, renaming, or removing a skill, agent, hook, or settings key.
