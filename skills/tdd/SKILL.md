---
name: tdd
description: "Use TDD whenever you add new features, modify existing functionality, and/or fix bugs."
---

# Test-Driven Development (TDD)

Tests are the executable specification of the software. Implementation is only justified by a specification; code written before its tests has no requirements to satisfy and is therefore pointless by definition.

## Workflow

1. Read `TESTING.md` for the repository's testing instructions.
2. Baseline: run the full test suite. If any test fails, stop immediately and report the failures. Proceed only on a fully green baseline.
3. Red: write or modify tests so they compile and fail for the intended reason. End-to-end, integration, and unit tests are all valid.
4. Green: implement the minimum functionality that makes the Red tests pass. Never weaken, remove, skip, or bypass tests to reach green.
5. Verify: run the full test suite. The baseline was green before any change, so every failure comes from your changes. Don't claim or speculate that a failure is pre-existing. If anything fails, diagnose it, fix it in Red, and repeat Red → Green → Verify until the suite is fully green.

Update the TODO list before starting, using this exact format:

```text
- [•] ⚪ Read: TESTING.md
- [ ] 🔵 Baseline: Running the full test suite
- [ ] 🔴 TDD Red: <New/modified end-to-end, integration, or unit tests that compile but fail>
- [ ] 🟢 TDD Green: <Minimum implementation that satisfies the Red tests>
- [ ] 🔵 Verification: Re-running the full test suite
```

## TDD Red Phase

* Tests compile and fail for the intended behavioral reason.
* Create or modify tests before implementing the corresponding behavior.
* Red tests specify the behavior the implementation must provide.
* Bug fixes start with a Red test that reproduces the reported symptom. If the test cannot reproduce it, investigate before changing production code.
* Assert exact expected values. When behavior is inherently variable, assert a range and state the reason in your report to the user, never in a code comment.
* Add production interfaces, types, or minimal skeletons only to make tests compile.
* Supporting code (enums, types, constants, null/argument guards, getters, wiring) needs no test of its own. Behavior tests cover it.

## TDD Green Phase

* Implement the simplest complete functionality that satisfies the Red tests.
* Preserve existing behavior unless the Red specification explicitly changes it.
* Don't weaken, remove, skip, disable, or modify Red tests to reach Green.
* Don't make unrelated production changes during Green.

## Test Design

* Tests are deterministic and independently repeatable.
* Test names are assertive, declarative, and describe the intended behavior.
* Tests are isolated and clean up the resources or external state they create.
* Tests specify observable behavior, not implementation details.
* Test names omit hedging and qualifiers, including `should`, `could`, `would`, `can`, `may`, `might`, `successfully`, `correctly`, `asExpected`, and equivalents.

## Test Value

Every test must give signal. It fails when something important breaks, such as behavior a caller or user relies on, or a domain invariant.

* Before writing a test, name the behavior or invariant it protects, or the realistic bug it would catch. If you can name neither, don't write the test.
* Prefer a few tests through the public interface over many tests of internals.
* Don't write tests that restate the code instead of specifying behavior:
  * an enum, constant, or config has the values just written;
  * a null, empty, or argument guard throws;
  * getters, setters, constructors, data classes, or default values;
  * a count (list length, rows, calls, SQL statements, created accounts). Assert the items or the observable outcome instead, or write no test;
  * a mock was called, when the observable outcome can be asserted;
  * language, framework, or library behavior.
  * migration version tests
* Don't add tests to raise coverage.
* Question every test: how likely is the scenario, and how strong is the signal? Remove tests for unlikely or weak scenarios.

## Existing Low-Value Tests

* When an existing test matches a forbidden pattern above and fails or needs changing, delete it instead of fixing it. List each deleted test in your report to the user.

## Layered Testing

* Start at the highest meaningful level. Exercise the requested behavior through public interfaces, abstractions, and real wiring.
* Add lower-level tests as implementation responsibilities and component boundaries become clear.
* Lower-level tests supplement, never replace, tests that specify the requested behavior at a higher level.
* Don't start with isolated unit tests as a substitute for specifying the behavior at the system level.

## Code Comments

* Express intent through names, structure, and executable specifications.
* Don't add comments to test code.
* Don't add comments to production code.

## Change Scope

* Keep each Red → Green cycle focused on the requested behavior.
* Don't mix unrelated refactoring, cleanup, or feature work into the cycle.
