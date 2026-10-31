#!/usr/bin/env python3
"""Subagent status line: show each agent row as '<type>  [model] <description>'.

Reads the subagentStatusLine JSON on stdin and prints one {"id", "content"} line per
task. A task without a model keeps Claude Code's default row.
"""
import json, re, sys

data = json.load(sys.stdin)
for task in data.get("tasks", []):
    model = task.get("model")
    if not model:
        continue
    short = re.sub(r"^claude-", "", model.split("/")[-1])  # strips the claude- prefix from the model id
    agent = task.get("agentType") or task.get("name") or ""
    text = task.get("description") or task.get("label") or ""
    content = f"{agent}  [{short}] {text}".strip()
    cols = data.get("columns")
    if isinstance(cols, int) and cols > 1 and len(content) > cols:
        content = content[: cols - 1] + "…"
    print(json.dumps({"id": task["id"], "content": content}))
