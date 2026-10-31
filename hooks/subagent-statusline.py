#!/usr/bin/env python3
"""Subagent status line: show each agent row as '[<model>] <description>'.

Reads the subagentStatusLine JSON on stdin and prints one {"id", "content"} line per
task. A tier model name (opus, sonnet, haiku) resolves through its
ANTHROPIC_DEFAULT_<TIER>_MODEL env var. A task without a model falls back to
CLAUDE_CODE_SUBAGENT_MODEL, then ANTHROPIC_MODEL. When no model can be determined the
row is the bare description. Rows are truncated to the "columns" width with an
ellipsis.
"""
import json, os, re, sys

TIER_ENV = {
    "opus": "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "sonnet": "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "haiku": "ANTHROPIC_DEFAULT_HAIKU_MODEL",
}


def short_model(value):
    """Strip a provider path, the claude- prefix, and the [1m] suffix."""
    value = value.rsplit("/", 1)[-1]
    value = re.sub(r"^claude-", "", value)
    return re.sub(r"\[1m\]$", "", value)


def resolve_model(value):
    """Resolve a tier name through its env var, then shorten the result."""
    if not value:
        return ""
    env = TIER_ENV.get(value.lower())
    if env:
        value = os.environ.get(env) or value
    return short_model(value)


def task_model(task):
    model = task.get("model")
    if model:
        return resolve_model(model)
    return resolve_model(
        os.environ.get("CLAUDE_CODE_SUBAGENT_MODEL") or os.environ.get("ANTHROPIC_MODEL")
    )


data = json.load(sys.stdin)
columns = data.get("columns")
for task in data.get("tasks", []):
    text = task.get("description") or task.get("label") or ""
    model = task_model(task)
    content = f"[{model}] {text}" if model else text
    if isinstance(columns, int) and columns > 1 and len(content) > columns:
        content = content[: columns - 1] + "…"
    print(json.dumps({"id": task["id"], "content": content}))
