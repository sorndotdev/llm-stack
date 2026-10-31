#!/usr/bin/env python3
"""Block any tool call that would publish a claude.ai session or chat link.

Covers git commits, gh PR/issue/comment/API calls, curl, and every MCP tool
(Slack, Gmail, Docs, ...). Read-only shell searches for the string are allowed.
"""

import json
import re
import sys

LINK = re.compile(r"claude\.ai/(code/)?(session_|chat/)")
PUBLISHING_SHELL = re.compile(r"\b(git\s+(commit|tag|notes|push)|gh\s+|curl\b|wget\b)")

event = json.load(sys.stdin)
tool = event.get("tool_name", "")
payload = json.dumps(event.get("tool_input", {}))

if not LINK.search(payload):
    sys.exit(0)

if tool == "Bash":
    command = event.get("tool_input", {}).get("command", "")
    if not PUBLISHING_SHELL.search(command):
        sys.exit(0)

print(
    "Blocked: this call contains a claude.ai session/chat link. Never publish session "
    "links in commits, PR bodies, issues, comments or messages. Remove the link "
    "(e.g. the 'Claude-Session:' trailer or the session URL line) and retry.",
    file=sys.stderr,
)
sys.exit(2)
