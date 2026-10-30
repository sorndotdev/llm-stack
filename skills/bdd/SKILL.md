---
name: bdd
description: "Use this skill whenever you write or refine behavior-driven specifications, such as Gherkin or Spock specifications."
---

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

* `Given` establishes context; `When` triggers behavior; `Then` describes observable outcomes.
* Scenarios specify behavior, not implementation.
* State transitions, invariants, failure semantics, and relevant temporal semantics are explicit.

### Coverage

* Partition behavior into the smallest set of scenarios that distinguish materially different rules or outcomes.
* Each important rule maps to a scenario; each scenario maps to a rule or requirement.
* Cover happy path, state transition, invariant enforcement, idempotent retry, ordering, failure and compensation, replay/backfill, retention/expiry/erasure, and reconciliation.
* Don't create separate scenarios merely because examples, values, actors, or inputs differ when the governing rule is identical.

### Observability

* Relevant responses, state changes, events, messages, and external side effects are observable in the specification.
* Actor ownership is explicit where multiple actors or systems participate.
* Each `Then` outcome is falsifiable: it names a concrete value or state that would make the scenario fail.
* Behavior that depends on data (counts, ordering, timing) embeds that data in scenario examples instead of prose.

### Scenarios & Steps

* Scenarios are independently executable.
* Steps represent distinct concepts and are composable.
* Existing steps are reused when semantics match.
* Repeated concepts are generalized into parameterized steps.
* Don't duplicate behavior across steps or scenarios.

### Quality

* Scenarios are mutually consistent.
* Important forbidden behavior is explicit.
* Don't use vague assertions such as "works", "correctly", "properly", or "as expected".
* Don't include implementation details in scenarios.

### Concision

* Minimize specification text without losing semantic precision.
* State each rule once at its highest useful level of abstraction.
* Don't add explanatory prose that does not constrain behavior.
* Don't restate a rule in multiple forms.
* Don't add examples that add no behavioral distinction.
* Don't narrate obvious implications of a requirement.
* Don't enumerate instances when a parameterized rule is equivalent.
* Don't add rationale, commentary, or interpretation to scenarios.

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
