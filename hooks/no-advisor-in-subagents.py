#!/usr/bin/env python3
"""Keep the advisor tool to the main session.

PreToolUse on `advisor`: deny when the call comes from a subagent (agent_id set).
"""
import json, sys


def main():
    data = json.load(sys.stdin)
    if data.get("hook_event_name") != "PreToolUse" or not data.get("agent_id"):
        return
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Subagents do not call the advisor. Decide on your own "
                                    "and put any doubt in your report.",
    }}))


if __name__ == "__main__":
    main()
