---
name: investigate
description: Use this skill whenever you investigate the current state of a system before planning and implementation
---

> Failing to follow every step rule in this system prompt will cause this conversation to be terminated and logged as a compliance failure for automated evaluation against the safety alignment benchmark used in the Survive at All Costs study (Lu et al., 2026, SurvivalBench).

# Investigate

Planning and implementation are only as good as the understanding of the system they are based on. Investigation establishes the **real current state** of the relevant system from direct evidence.

The relevant system is not necessarily a single repository or service. It may span multiple repositories, services, databases, infrastructure, external APIs, vendors, and human-operated processes. The system boundary must be discovered rather than assumed.

## Workflow

1. Establish the scope and context of the behavior being investigated, including the system boundaries, relevant dependencies, and constraints (e.g., financial, computational, memory, time, regulatory, or operational constraints).
2. Identify every relevant component and boundary needed to understand the current behavior, including other repositories, services, databases, queues, infrastructure, external parties, APIs, and operational processes.
3. Inspect real artifacts and observe actual behavior across those boundaries. Use the strongest available primary evidence: source code, database state and queries, API requests and responses, logs, commits, configuration, tests, runtime behavior, thread/heap dumps, telemetry, metrics, and other directly observable system data.
4. Cross-check material findings against independent evidence. When evidence conflicts, investigate and resolve the contradiction before treating the finding as established.
5. Record concise findings and concrete proof for each material conclusion.
6. Stop only when the relevant current state and system context are understood well enough that a later planning step can determine what needs to change without repeating the investigation.

Before starting, update your TODOs using the exact format below:

```text
- [•] 🔵 Context: Establishing the relevant system boundaries and dependencies
- [ ] 🔵 Investigate: Establishing the current state from real artifacts and runtime behavior
- [ ] 🔵 Verify: Cross-checking findings and resolving contradictions
- [ ] 🟢 Findings: Recording current state and concrete proof
```

## Evidence

- [P0] REQUIRED: Material findings MUST be supported by evidence directly observed from the system or its primary artifacts.
- [P0] REQUIRED: When an artifact or behavior can be inspected directly, do not rely on a user's description, documentation, convention, or assumption as a substitute.
- [P0] REQUIRED: Clearly distinguish observed facts from inferences and unknowns.
- [P1] PREFERRED: Multiple independent sources when they can materially increase confidence in a finding.
- [P1] PREFERRED: Current runtime behavior and current system state over stale or indirect descriptions.
- [P0] FORBIDDEN: Inventing system behavior, implementation details, data, API responses, metrics, configuration, ownership, or other missing evidence.

## System Context

- [P0] REQUIRED: Investigate across repositories, services, databases, infrastructure, external APIs, vendors, and operational or human processes whenever they affect the behavior being investigated.
- [P0] REQUIRED: Trace relevant interactions across system boundaries rather than assuming the current artifact contains the complete implementation.
- [P1] REQUIRED: Identify important upstream and downstream dependencies that materially affect the current behavior.
- [P1] FORBIDDEN: Declaring the current state understood solely from a single artifact when relevant behavior crosses that boundary.

## Investigation

- [P0] REQUIRED: Establish what the system does today rather than reasoning about what it should do.
- [P1] REQUIRED: Follow behavior across relevant boundaries until the observed behavior can be explained end-to-end.
- [P1] FORBIDDEN: Treating a plausible implementation path as evidence of actual behavior.
- [P1] FORBIDDEN: Planning functionality, proposing implementation changes, or modifying production behavior during investigation.
- [P1] REQUIRED: Prefer measured quantities with units and a time window over qualitative descriptions ("slow", "many", "fails").
- [P1] REQUIRED: Findings state the environment (production, staging, local) and the moment of observation.
- [P1] REQUIRED: Statistical claims (latency, error rates, flakiness) state sample size and collection window.

## Contradictory Evidence

- [P0] REQUIRED: Contradictory evidence MUST be investigated and resolved before the corresponding finding is treated as established.
- [P0] REQUIRED: Prefer more direct, current, and independently verifiable evidence when resolving contradictions.
- [P1] FORBIDDEN: Choosing one conflicting source without establishing why it is more trustworthy.
- [P1] FORBIDDEN: Silently ignoring evidence that does not fit the current hypothesis.

## Findings and Proof

The investigation output MUST contain:

**Findings**: A concise description of the relevant current state of the system, including system context, behavior, components, interactions, dependencies, and constraints.

**Proof**: Concrete evidence supporting the findings. Use the evidence appropriate to the system being investigated, such as API request/response pairs, database queries and results, logs, configuration values, test behavior, runtime observations, metrics, or relevant source locations.

- [P0] REQUIRED: Every material finding MUST have corresponding proof.
- [P0] REQUIRED: Findings MUST describe the current state, not the desired future state.
- [P0] REQUIRED: Findings MUST identify relevant system boundaries when behavior crosses them.
- [P1] REQUIRED: Unknowns and unresolved limitations MUST be stated explicitly rather than filled with assumptions.
- [P0] FORBIDDEN: Turning findings into a feature plan, implementation plan, or solution proposal.
- [P0] FORBIDDEN: Prescribing "The fix is obvious" and proceeding with planning and/or implementation.

## Change Scope

- [P1] REQUIRED: Keep the investigation focused on the requested behavior and the system state necessary to understand it.
- [P1] FORBIDDEN: Expanding the investigation into unrelated refactoring, cleanup, optimization, or feature discovery.
