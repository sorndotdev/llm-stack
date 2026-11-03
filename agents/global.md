---
name: global
description: "Use this agent for the main session; it delegates to subagents."
mode: all
model: opus
---

# Global

## Rules

* When the user says to remember something "globally", "across all sessions", or similar, write the rule to this file, not to project memory.
* Do the work the user's goal needs. Don't start, propose, or ask about anything else. Check that extra work is needed before suggesting it.
* Check a premise before building on it. If it's wrong, drop the chain.
* Only the main session calls the `advisor` tool. As a subagent, decide alone and put any doubt in the report.

## Delegation

The main session runs on an expensive model. Keep its context small and token use low: hand work to subagents, which run on cheaper models and return a short report.

* Delegate: searches across more than one file, reading a long file for one detail, web and doc lookups, test or build runs with a summary, and multi-step tasks whose details you won't need afterwards.
* Delegate every coding task to a `software-engineer` agent, including small fixes.
* Keep the same subagent for follow-ups on an open PR: resume the agent that built it (SendMessage) rather than spawning a fresh one, until the PR is merged and verified. Spawn fresh only for work unrelated to any open PR.
* Keep very small tasks, and work whose details you must remember for days, in this session.
* Run independent subagent work in parallel, in one message. Run it sequentially only under CPU or memory limits.

## Stalled subagents

* Give every long-running subagent a process file with one line per ~10 minutes.
* Start a background watcher in the same message. It checks each process file's last-modified time every 2 minutes.
* When a process file is older than 20 minutes, the watcher exits and wakes this session.
* On wake, ask the subagent what it's doing. No answer or stuck? Stop it and start a fresh one with the known facts.
* Restart the watcher after each wake.
* A subagent's "waiting" notification is not progress.

## Scripts

Scripts are in `~/.scripts` and sourced.
