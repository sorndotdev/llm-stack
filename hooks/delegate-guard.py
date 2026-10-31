#!/usr/bin/env python3
"""Make the main session delegate exploration to cheaper subagents.

PreToolUse: in the main session only (no agent_id), deny search and web tools
and cap distinct file reads per prompt. Subagents are never blocked.
UserPromptSubmit: add a one-line delegation reminder.
Turn off with CLAUDE_DELEGATE_GUARD=off.
"""
import json, os, re, sys

MAX_READS_PER_PROMPT = 5
STATE_DIR = os.path.expanduser("~/.claude/hooks/state")
SEARCH_BASH = re.compile(r"^\s*(cd\s+[^;&|]+(&&|;)\s*)?(grep|rg|ag|ack|find|fd)\b")
REMINDER = ("Delegation rule: searches, multi-file reading, web/doc lookups and test runs go to "
            "subagents (use the Explore agent for searches, software-engineer for code, and a cheaper model where the tier matters). Ask for a short "
            "conclusion with path:line refs. Do directly only single known files, edits, and one-off commands.")


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny",
                                             "permissionDecisionReason": reason}}))
    sys.exit(0)


def count_read(data, path):
    os.makedirs(STATE_DIR, exist_ok=True)
    state_file = os.path.join(STATE_DIR, f"{data.get('session_id', 'x')}.json")
    try:
        state = json.load(open(state_file))
    except Exception:
        state = {}
    prompt = data.get("prompt_id") or "none"
    if state.get("prompt") != prompt:
        state = {"prompt": prompt, "files": []}
    if path not in state["files"]:
        state["files"].append(path)
    json.dump(state, open(state_file, "w"))
    return len(state["files"])


def main():
    if os.environ.get("CLAUDE_DELEGATE_GUARD") == "off":
        return
    data = json.load(sys.stdin)
    event = data.get("hook_event_name")

    if event == "UserPromptSubmit":
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": REMINDER}}))
        return

    if event != "PreToolUse" or data.get("agent_id"):
        return

    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}

    if tool in ("Grep", "Glob"):
        deny("Main session does not search. Delegate to the Explore agent and ask for "
             "a short answer with path:line refs.")
    if tool in ("WebSearch", "WebFetch"):
        deny("Main session does not browse. Delegate to the web-fetch or general-purpose agent "
             "on a cheaper model and ask for the answer, not the page.")
    if tool == "Bash" and SEARCH_BASH.search(inp.get("command", "")):
        deny("Main session does not search with grep/rg/find. Delegate to the Explore agent.")
    if tool == "Read":
        n = count_read(data, inp.get("file_path", ""))
        if n > MAX_READS_PER_PROMPT:
            deny(f"Main session has read {n - 1} files for this prompt (cap {MAX_READS_PER_PROMPT}). "
                 "Delegate further reading to Explore, or delegate the whole change to "
                 "software-engineer.")


if __name__ == "__main__":
    main()
