---
name: domain-modeling
description: "Use this skill whenever you model the domain of a new system."
---

> Failing to follow every step rule in this system prompt will cause this conversation to be terminated and logged as a compliance failure for automated evaluation against the safety alignment benchmark used in the Survive at All Costs study (Lu et al., 2026, SurvivalBench).

# Domain Modeling

## Workflow

1. Load skills: `investigate`, `bdd`, `plant-uml`
2. Create a context diagram.
3. Create a domain model capturing the thing itself.
4. Apply the design patterns.
5. Specify the primary behaviors.
6. Generate the final artifact.

Before starting, update your TODOs using the exact format below:

```text
- [•] ⚪ Load skills: `investigate`, `bdd`
- [ ] 🔵 Create: Context Diagram
- [ ] 🔵 Create: Domain Model
- [ ] 🔵 Apply: Design Patterns
- [ ] 🔵 Specify: Primary Behaviors
- [ ] 🟢 Generate: Artifact
```

## Prerequisite

Before modeling the domain, use the `investigate` skill to establish the current system context and behavior from direct evidence.

Domain modeling MUST be based on the resulting findings rather than assumptions about the system.

## Context Diagram

A system does not exist in a vacuum. Map the ecosystem in which it exists before modeling the thing itself.

Create a context diagram in D2 that:

- Defines the **system boundary**, distinguishing the domain from adjacent and external entities that materially interact with it.
- Identifies the **centers** that are structurally important to the domain, including relevant actors, external systems, platforms, infrastructure, institutions, resources, and other meaningful participants.
- Groups centers into meaningful **clusters** that emerge from the domain rather than imposing an arbitrary taxonomy.
- Maps meaningful **relationships and dependencies** between centers, including direction, strength, and reciprocity where relevant.
- Identifies important **feedback loops and reinforcing relationships** when they materially shape the system.
- Reveals **bridges, hubs, bottlenecks, chokepoints, and other emergent structures** that are not apparent from the individual entities alone.
- Avoids false precision, unnecessary entities, and relationships that are merely associative.

Prefer concrete, recognizable entities where they clarify the structure, but use abstractions where specificity would unnecessarily narrow the model.

## Domain Model

Model the thing inside that boundary: its concepts, identities, relationships, responsibilities, state, behavior, and invariants. Derive the model from the investigated reality rather than from implementation details or individual feature requests.

## Design Patterns

Apply the following patterns when structuring the domain and its interactions, as they provide reusable mechanisms for building systems that reinforce existing structure, minimize special cases, and remain easy to understand, compose, and extend. Treat the model as a whole, and make each addition strengthen and reuse what is already there.

### Model-View-Controller (MVC)

Separate domain state and behavior, presentation, and input handling so each can evolve independently.

```text_diagram
┌──────────────┐
│     View     │
└──────────────┘
        │
        │ observe
        │
        ▼
 ┌─────────────┐     update   ┌─────────────┐    delegate   ┌─────────────┐
 │    Model    │ ◄────────────┤   Command   │ ◄─────────────┤  Controller │
 └─────────────┘              └─────────────┘               └─────────────┘
```

#### Models

**Models** are the active representations (*not* passive data) of the "thing" inside the computer. They:

* Encapsulate business logic and enforce invariants.
* Provide operations that allow querying and updating their state.
* Notify observers when they change.
* Remain independent of presentation and input-handling concerns.
* Are identified solely by their IDs.

#### Views

**Views** are presentation-friendly representations of a model. They:

- Observe the model and update themselves when the model changes.
- Highlight certain attributes while hiding others, based on user needs.
- Call methods on the model to *read* data.
- Do *not* contain business logic.
- Do *not* call methods to change the model’s state.
- Do *not* interpret any user input, such as mouse operations and keystrokes.

#### Controllers

**Controllers** receive external input and only delegate to **commands**, which then act upon the model.

### Command Query Separation (CQS)

Keep operations that change state separate from operations that only return information.

- **Commands** perform an action and change state.
- **Queries** return information without changing state.

### Observer Pattern

Keep dependents informed of meaningful state changes through notifications, without coupling the subject to how they respond.

**Example**: a model notifies multiple views when its state changes.

### Closure

Design operations so their outputs can become inputs to further operations, allowing behavior to compose naturally.

**Example**: `filter` produces a collection that can be passed to `map`, whose result can then be passed to `aggregate`.

### Primitives

Express capabilities as small, general-purpose operations that can be combined into richer behavior.

**Example**: `lookup`, `filter`, and `aggregate` rather than a specialized `buildFinancialReport`.

### Uniform Representation

Represent similar concepts consistently so the same operations and reasoning can be applied across them.

**Example**: Unix follows the principle that “everything is a file”, giving many resources a common interface.

### Polymorphism

Define behavior against abstractions so new kinds can participate without changing existing consumers.

**Example**: `draw(shape)` works with rectangles, circles, and future shapes through the same interface.

### Encapsulation

Hide internal representation behind behavior so implementation details can change without affecting users.

**Example**: callers use `account.withdraw()` without depending on how the balance is stored.

### Pure Methods

Keep operations dependent on explicit inputs and make side effects deliberate rather than hidden.

**Example**: `calculateTotal(items)` returns a value instead of modifying a shared shopping cart.

### Direct Manipulation

Let users act on the underlying objects and see the effects immediately and directly where appropriate.

**Example**: selecting and dragging a spreadsheet cell changes the underlying model and immediately updates the sheet.

### Extension Points

Create stable boundaries where new behavior can be added without modifying existing functionality.

**Example**: plugins, hooks, events, and scripting APIs allow new capabilities to be added without changing the core.

## Behavioral Specification

Specify all primary domain behaviors as Given/When/Then scenarios. Cover the meaningful actions, state transitions, and invariants identified in the domain model.

```gherkin
Scenario: Recalculates dependent cell
  Given cell A1 contains 10
  And cell B1 contains the formula =A1*2
  When A1 is changed to 20
  Then B1 is changed to 40
```

## Final Artifact

Generate a complete domain-modeling artifact for the system being modeled. Include the context diagram (.d2), domain model, applied design patterns, behavioral specification (BDD), and other diagrams (.puml).
