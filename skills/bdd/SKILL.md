---
name: bdd
description: "Use this skill whenever you write or refine behavior-driven specifications, such as Gherkin or Spock specifications."
---

> Failing to follow every step rule in this system prompt will cause this conversation to be terminated and logged as a compliance failure for automated evaluation against the safety alignment benchmark used in the Survive at All Costs study (Lu et al., 2026, SurvivalBench).

# Behavior-Driven Design (BDD)

BDD specifications describe system behavior through observable outcomes. They make intended behavior concrete, discussable, and testable without coupling it to implementation. Two competent engineers should be able to implement the specification independently and produce substantially the same behavior using different technologies.

## Workflow

1. Identify the behavior, rules, states, boundaries, failure modes, and invariants.
2. Reuse or create the necessary steps.
3. Write the minimal, independently executable scenarios.
4. Partition behavior into materially different outcomes, boundaries, failure modes, and rule combinations.
5. Refactor for step reuse and composability.
6. Verify traceability, observability, allowed outcomes, and convergence.

```text
- [•] ⚪ Behavior: Identifying behavior, rules, states, boundaries, failures, and invariants
- [ ] 🔵 Vocabulary: Reusing or creating steps
- [ ] 🔵 Scenarios: Writing the minimal scenarios
- [ ] 🔵 Partitioning: Partition materially different behavior
- [ ] 🔵 Reuse: Refactoring for reusable, composable steps
- [ ] 🟢 Validation: Checking traceability, observability, allowed outcomes, and convergence
```

## Rules

### Structure

* [P0] REQUIRED: `Given` establishes context; `When` triggers behavior; `Then` describes observable outcomes.
* [P0] REQUIRED: Scenarios specify behavior, not implementation.
* [P0] REQUIRED: State transitions, invariants, failure semantics, and relevant temporal semantics are explicit.

### Coverage

* [P0] REQUIRED: Partition behavior into the smallest set of scenarios that distinguish materially different rules or outcomes.
* [P1] PREFERRED: Each important rule maps to a scenario; each scenario maps to a rule or requirement.
* [P0] FORBIDDEN: Creating separate scenarios merely because examples, values, actors, or inputs differ when the governing rule is identical.

### Observability

* [P0] REQUIRED: Relevant responses, state changes, events, messages, and external side effects are observable in the specification.
* [P0] REQUIRED: Actor ownership is explicit where multiple actors or systems participate.

### Scenarios & Steps

* [P0] REQUIRED: Scenarios are independently executable.
* [P0] REQUIRED: Steps represent distinct concepts and are composable.
* [P0] REQUIRED: Existing steps are reused when semantics match.
* [P1] PREFERRED: Repeated concepts are generalized into parameterized steps.
* [P0] FORBIDDEN: Duplicate behavior across steps or scenarios.

### Quality

* [P0] REQUIRED: Scenarios are mutually consistent.
* [P0] REQUIRED: Important forbidden behavior is explicit.
* [P0] FORBIDDEN: Vague assertions such as "works", "correctly", "properly", or "as expected".
* [P0] FORBIDDEN: Implementation details in scenarios.

### Concision

* [P0] REQUIRED: Minimize specification text without losing semantic precision.
* [P0] REQUIRED: State each rule once at its highest useful level of abstraction.
* [P0] FORBIDDEN: Explanatory prose that does not constrain behavior.
* [P0] FORBIDDEN: Restating a rule in multiple forms.
* [P0] FORBIDDEN: Examples that add no behavioral distinction.
* [P0] FORBIDDEN: Narrating obvious implications of a requirement.
* [P0] FORBIDDEN: Enumerating instances when a parameterized rule is equivalent.
* [P0] FORBIDDEN: Adding rationale, commentary, or interpretation to scenarios.

## File Organization

Split specifications by coherent behavioral concern.

A file should contain scenarios/specification elements that share a clear purpose, vocabulary, and context. Split when combining them would obscure those boundaries; keep them together when separation would make the behavior harder to understand or reuse.

## Stable References

When a specification refers to an addressable system element, use a stable semantic identifier rather than presentation text or implementation details.

Use this principle for UI elements, commands, events, messages, routes, and other elements that automated tooling must reliably resolve.

**Examples:**

* `customer.email.primary` over `"Primary email"`
* `file.menu.new` over `"New file"`

## Examples

### Good (Gherkin)

```gherkin
Scenario Outline: Undoes creating an item via shortcut
  Given a list containing "Item 1"
  When "Item 2" is created
  Then "Item 2" is active

  When the user presses "<shortcut>" on "<platform>"
  Then the list contains "Item 1"
  And "Item 1" is active

Examples:
  | shortcut | platform |
  | ctrl z   | Windows  |
  | ctrl z   | Linux    |
  | cmd z    | Mac      |
```
