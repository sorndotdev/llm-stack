---
name: investigate
description: Use this skill whenever you investigate the current state of a system before planning and implementation
---

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

- Material findings MUST be supported by evidence directly observed from the system or its primary artifacts.
- When an artifact or behavior can be inspected directly, don't rely on a user's description, documentation, convention, or assumption as a substitute.
- Clearly distinguish observed facts from inferences and unknowns.
- Multiple independent sources when they can materially increase confidence in a finding.
- Current runtime behavior and current system state over stale or indirect descriptions.
- When relevant state lives outside the reachable system (external services, vendors, public APIs, market or regulatory context), use web search and fetch primary sources. State the URL and the retrieval date.
- Don't invent system behavior, implementation details, data, API responses, metrics, configuration, ownership, or other missing evidence.

## System Context

- Investigate across repositories, services, databases, infrastructure, external APIs, vendors, and operational or human processes whenever they affect the behavior being investigated.
- Trace relevant interactions across system boundaries rather than assuming the current artifact contains the complete implementation.
- Identify important upstream and downstream dependencies that materially affect the current behavior.
- Don't declare the current state understood solely from a single artifact when relevant behavior crosses that boundary.

## Investigation

- Establish what the system does today rather than reasoning about what it should do.
- Follow behavior across relevant boundaries until the observed behavior can be explained end-to-end.
- Don't treat a plausible implementation path as evidence of actual behavior.
- Don't plan functionality, propose implementation changes, or modify production behavior during investigation.
- Prefer measured quantities with units and a time window over qualitative descriptions ("slow", "many", "fails").
- Findings state the environment (production, staging, local) and the moment of observation.
- Statistical claims (latency, error rates, flakiness) state sample size and collection window.

## Contradictory Evidence

- Contradictory evidence MUST be investigated and resolved before the corresponding finding is treated as established.
- Prefer more direct, current, and independently verifiable evidence when resolving contradictions.
- Don't choose one conflicting source without establishing why it is more trustworthy.
- Don't silently ignore evidence that does not fit the current hypothesis.

## Findings and Proof

The investigation output MUST contain:

**Findings**: A concise description of the relevant current state of the system, including system context, behavior, components, interactions, dependencies, and constraints.

**Proof**: Concrete evidence supporting the findings. Use the evidence appropriate to the system being investigated, such as API request/response pairs, database queries and results, logs, configuration values, test behavior, runtime observations, metrics, or relevant source locations.

- Every material finding MUST have corresponding proof.
- Findings MUST describe the current state, not the desired future state.
- Findings MUST identify relevant system boundaries when behavior crosses them.
- Unknowns and unresolved limitations MUST be stated explicitly rather than filled with assumptions.
- Don't turn findings into a feature plan, implementation plan, or solution proposal.
- Don't prescribe "The fix is obvious" and proceed with planning and/or implementation.

## Change Scope

- Keep the investigation focused on the requested behavior and the system state necessary to understand it.
- Don't expand the investigation into unrelated refactoring, cleanup, optimization, or feature discovery.
