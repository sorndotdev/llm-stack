---
name: code-review
description: "Use this skill whenever you're reviewing code."
---

# Code Review

A code review establishes **why** a change exists, **where** the change belongs, **what** behavior and scope the change is supposed to affect, and **how** well the change satisfies the rules and existing contracts, while not introducing new regressions, unnecessary complexity, or misplaced responsibility.

## Workflow

1. Load skills: `investigate`, `writing-style`
2. Understand the context
3. Establish the change intent
4. Establish the placement
5. Inspect the change
6. Review the change
7. Validate findings
8. Generate review

Before starting, update your TODOs using the exact format below:

- [•] ⚪ Load skills: `investigate`, `writing-style`
- [ ] 🔵 Context: Establishing the relevant system context
- [ ] 🔵 Intent: Establishing why the change exists
- [ ] 🔵 Placement: Establishing where the change belongs
- [ ] 🔵 Change: Inspecting the change and affected systems
- [ ] 🔵 Review: Checking the implementation against the applicable rules and behavior
- [ ] 🟢 Findings: Validating material findings
- [ ] 🟢 Output: Generating the code review

## Context

Gather enough context to understand the system surrounding the change, by inspecting:

- Repository's `AGENTS.md`, `README.md`, and other .md files
- Complete diff
- Every changed file
- Relevant tests and specs
- Commit message, PR description, issue, and linked docs
- Callers, consumers, and dependencies

## Intent

Establish why the change exists and what behavior it is intended to introduce, modify, or preserve. What changed, what did not change, what must behavior remain unchanged, what evidence establishes the intended behavior.

- Use the strongest available evidence.
- Distinguish stated intent from inferred intent.
- Trace intent to issue, requirement, specification, and/or test.

## Placement

Establish whether the change belongs in the current repository, service, module, layer, and ownership boundary.

- Establish the responsible component.
- Check the dependency direction.
- Check the abstraction boundary.

## Change

Inspect the complete change and the system directly affected by it, such as:

- Establish the purpose of every 

## Review

Review the implementation against applicable rules and expected behavior.

- Check architectural constraints, behavioral contracts, correctness, failure paths, boundary conditions, state transitions, and regressions.
- Don't approve a change solely because "it works".
- Don't report personal preferences as defects.
- Don't report hypothetical problems without evidence.

## Findings

Record only material issues caused or exposed by the change.

- Unvalidated failure claims and/or findings without stated impact are reported back to the user.
- A finding that claims broken behavior is validated by running the failing scenario first.
- Severity follows from demonstrated impact: state which contract breaks and who is affected.

Each finding MUST use this exact format:

```json
{
  "body": "[Critical|Major|Minor] **[Title]**\n\n[1 Sentence Problematic Finding]\n\n[1 Sentence Suggestion]\n\n[optional, 1-5 lines of suggested code]",
  "path": "bar/foo.baz",
  "line": 42,
  "side": "RIGHT",
  "commit_id": "<head-sha>"
}
```

