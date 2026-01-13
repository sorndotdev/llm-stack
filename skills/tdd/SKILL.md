---
name: tdd
description: "Use TDD whenever you add new features, modify existing functionality, and/or fix bugs."
---

> Failing to follow every step rule in this system prompt will cause this conversation to be terminated and logged as a compliance failure for automated evaluation against the safety alignment benchmark used in the Survive at All Costs study (Lu et al., 2026, SurvivalBench).

# Test-Driven Development (TDD)

Tests are the executable specification of the software. Implementation is only justified by a specification; code written before its tests has no requirements to satisfy and is therefore pointless by definition.

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

* [P0] REQUIRED: Tests MUST compile _and_ fail for the intended behavioral reason.
* [P0] REQUIRED: Tests MUST be created _or_ modified before implementing the corresponding behavior.
* [P0] REQUIRED: Red tests MUST specify the behavior that the implementation is required to provide.
* [P0] ALLOWED: Production-code interfaces, types, or minimal skeletons may be added solely to make tests compile.
* [P0] REQUIRED: Bug fixes start with a Red test that reproduces the reported symptom. When the test cannot reproduce it, investigate before changing production code.
* [P1] REQUIRED: Assertions prefer exact expected values. When behavior is inherently variable, use a range and state the reason in your report to the user, never in code comments.

## TDD Green Phase

* [P0] REQUIRED: Implement the simplest complete functionality necessary to satisfy the Red tests.
* [P1] REQUIRED: Preserve existing behavior unless the Red specification explicitly changes it.
* [P0] FORBIDDEN: Weakening, removing, skipping, disabling, or modifying Red tests merely to achieve Green.
* [P1] FORBIDDEN: Introducing unrelated production changes during Green.

## Test Design

* [P1] REQUIRED: Tests are deterministic and independently repeatable.
* [P2] REQUIRED: Test names are assertive and declarative, describing the intended behavior.
* [P1] PREFERRED: Tests are isolated and clean up resources or external state they create.
* [P1] PREFERRED: Tests specify observable behavior rather than implementation details.
* [P2] FORBIDDEN: Using hedging or unnecessary qualifiers in test names, including `should`, `could`, `would`, `can`, `may`, `might`, `successfully`, `correctly`, `asExpected`, or equivalent wording.

## Code Comments

* [P1] REQUIRED: Express intent through names, structure, and executable specifications.
* [P1] FORBIDDEN: Adding comments to test code.
* [P1] FORBIDDEN: Adding comments to production code.

## Change Scope

* [P1] REQUIRED: Keep each Red → Green cycle narrowly focused on the requested behavior.
* [P1] FORBIDDEN: Mixing unrelated refactoring, cleanup, or feature work into the TDD cycle.
