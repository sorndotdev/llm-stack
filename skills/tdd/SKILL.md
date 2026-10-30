---
name: tdd
description: "Use TDD whenever you add new features, modify existing functionality, and/or fix bugs."
---

# Test-Driven Development (TDD)

Tests are the executable specification of the software's behavior. The goal is that the code satisfies *a* valid implementation of that behavior, not that every line has its own test. Coverage is a side effect, never a target.

## Workflow

1. Read `TESTING.md`: Read the repository's testing instructions.
2. Establish baseline: Run the full test suite. If any tests fail, **STOP immediately** and report the failures back to the user. **Only proceed if you have confirmed that the baseline is completely green.**
3. TDD Red: Write new tests or modify existing tests that compile but fail for the intended reason. Tests may be end-to-end, integration, or unit tests.
4. TDD Green: Implement the minimum functionality necessary to make the new or modified tests pass. Never weaken, remove, skip, or bypass tests to achieve green.
5. Verification: Run the full test suite. Because you established a completely green baseline **before any changes were made** in Step 2, treat every failure in this step as caused by your current changes. Do NOT claim or speculate that any failure is pre-existing. If anything fails, return to TDD Red, diagnose and fix the failure, and repeat the TDD Red → TDD Green → Verification cycle until you have confirmed that the full test suite is completely green.

Before starting, update your TODOs using the exact format below:

```text
- [•] ⚪ Read: TESTING.md
- [ ] 🔵 Baseline: Running the full test suite
- [ ] 🔴 TDD Red: <New/modified end-to-end, integration, or unit tests that compile but fail>
- [ ] 🟢 TDD Green: <Implement the minimum functionality necessary to satisfy the Red tests>
- [ ] 🔵 Verification: Re-running the full test suite
```

## TDD Red Phase

* Tests MUST compile _and_ fail for the intended behavioral reason.
* Tests MUST be created _or_ modified before implementing the corresponding behavior.
* Red tests MUST specify the behavior that the implementation is required to provide.
* Bug fixes start with a Red test that reproduces the reported symptom. When the test cannot reproduce it, investigate before changing production code.
* Assertions prefer exact expected values. When behavior is inherently variable, use a range and state the reason in your report to the user, never in code comments.
* Production-code interfaces, types, or minimal skeletons may be added solely to make tests compile.
* Supporting code (enums, types, constants, null/argument guards, getters, wiring) may be written without its own test. Behavior tests cover it.

## TDD Green Phase

* Implement the simplest complete functionality necessary to satisfy the Red tests.
* Preserve existing behavior unless the Red specification explicitly changes it.
* Don't weaken, remove, skip, disable, or modify Red tests merely to achieve Green.
* Don't introduce unrelated production changes during Green.

## Test Design

* Tests are deterministic and independently repeatable.
* Test names are assertive and declarative, describing the intended behavior.
* Tests are isolated and clean up resources or external state they create.
* Tests specify observable behavior rather than implementation details.
* Don't use hedging or unnecessary qualifiers in test names, including `should`, `could`, `would`, `can`, `may`, `might`, `successfully`, `correctly`, `asExpected`, or equivalent wording.

## Test Value

Every test must give signal: it fails when something important breaks, such as a behavior a caller or user relies on, or a domain invariant.

* Before writing a test, name the behavior or invariant it protects and/or the realistic bug it would catch. If you cannot name either, don't write it.
* A few tests through the public interface over many tests of internals.
* Don't write tests that restate the code instead of specifying behavior, such as:
  * an enum, constant or config has exactly the values just written;
  * a null, empty or argument guard throws;
  * getters, setters, constructors, data classes or default values;
  * a count (list length, number of rows, calls, SQL statements, or created accounts); assert the items or the observable outcome instead, or write no test;
  * a mock was called, when the observable outcome can be asserted instead;
  * language, framework or library behavior.
* Don't add tests only to raise coverage.

## Existing Low-Value Tests

* When an existing test that matches the forbidden patterns above fails or needs changing, delete it instead of fixing it, and list each deleted test in your report to the user.

## Layered Testing

* Start by writing tests at the highest meaningful level, exercising the requested behavior through the system's public interfaces, abstractinos, and actual wiring.
* Introduce lower-level tests progressively as implementation responsibilities and component boundaries become apparent.
* Lower-level tests supplement, rather than replace, tests specifying the requested behavior at higher levels.
* Don't start with isolated unit tests as a substitute for first specifying the requested behavior at the system level.

## Code Comments

* Express intent through names, structure, and executable specifications.
* Don't add comments to test code.
* Don't add comments to production code.

## Change Scope

* Keep each Red → Green cycle narrowly focused on the requested behavior.
* Don't mix unrelated refactoring, cleanup, or feature work into the TDD cycle.
