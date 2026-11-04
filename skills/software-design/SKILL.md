---
name: software-design
description: "Use when designing a greenfield software project or deciding whether a new feature strengthens or harms the existing system."
---

# Software Design

Durable systems win by reinforcement, not accumulation. Each new feature must strengthen the features already present. That is the general concept to internalize. The properties and mechanisms below are examples of it, not the complete list.

## The Four Properties

The properties spell CODE.

- **Composability:** parts combine to create new capabilities.
- **Orthogonality:** a change in one area has no unexpected effects in another.
- **Discoverability:** users find and understand capabilities naturally.
- **Extensibility:** the system grows without breaking its foundation.

No single property is enough. Combined, they create synergy. The system becomes more than the sum of its parts. Spreadsheets have shipped since VisiCalc in 1979 and combine all four:

- **Composability:** formulas return values that other cells and formulas consume. Simple operations compose into complex models.
- **Orthogonality:** changing a cell's formatting does not change its value. Editing a formula does not change how the sheet displays.
- **Discoverability:** the whole model is visible and directly manipulable. Users inspect formulas and trace dependencies as they explore.
- **Extensibility:** custom functions, macros, plugins, scripts, and external data connections extend the sheet without changing the core model.

## Mechanisms

Properties describe what a durable system looks like. Mechanisms describe how the properties emerge. Some of the most important ones. There are more.

- **Closure:** can outputs become valid inputs for further operations? Example chain: input → output → input → output.
- **Primitives:** are capabilities exposed as small building blocks? Example: `lookup`, `aggregate`, `filter` rather than `financial report builder`.
- **Uniform representation:** is information represented the same way everywhere? Example: every spreadsheet value lives in a cell, every Unix resource is a file.
- **Pure methods:** do components depend only on their inputs rather than mutating shared state? Example: `calculateTotal(items)` returns a value rather than updating a global cart.
- **Polymorphism:** do components operate on abstractions rather than concrete implementations? Example: `draw(shape)` rather than `draw(rectangle)`, `draw(circle)`.
- **Encapsulation:** can components change internally without affecting their users? Example: changing a database implementation without changing the API.
- **Direct manipulation (HCI):** do users interact with the underlying model directly and see results immediately? Example: selecting, dragging, editing, and inspecting the objects themselves.
- **Extension points:** does the system provide stable places to add behavior without modifying existing functionality? Example: plugins, hooks, events, and scripting.

| Property | Enabling mechanisms |
| --- | --- |
| Composability | closure, primitives, uniform representation, polymorphism |
| Orthogonality | pure methods, encapsulation, polymorphism |
| Discoverability | direct manipulation, primitives |
| Extensibility | extension points, polymorphism |

## Compounding Systems

Features are not assets by themselves. They become assets only when they strengthen the capabilities already present. Durable products grow by increasing the meaningful interactions between features, not by accumulating features. The most enduring systems look surprisingly small. Their power comes from reinforcement, not addition.

- **Power users:** macros and shortcuts accelerate experts without adding features beginners must learn. One set of primitives serves both.

### Centers and Living Structure

Christopher Alexander formulated this in his 1996 talk [*Patterns in Architecture*](https://www.youtube.com/watch?v=98LdFA-_zfA) at ACM OOPSLA.

A **center** gains strength only through mutual reinforcement with other centers. Each center makes the others more coherent, as spreadsheet cells and formulas do. The CODE properties let each new feature intensify the centers already present. A feature is only as durable as the centers it intensifies.

Applied to software:

> Observe reality. Then make the smallest change that strengthens the current whole.
>
> Not: "What's the next feature?"
>
> But: "What did reality reveal? What is the smallest strengthening transformation?"

### Reflexivity

Reflexivity is built into the recursion of centers. Each structure-preserving step feeds the intensified whole back into observation. The system and its maker keep disclosing new weak centers from within. Living software regenerates its coherence through that closed loop of sensing and minimal transformation.

George Soros built his investment philosophy on the same principle in [*The Alchemy of Finance*](https://en.wikipedia.org/wiki/The_Alchemy_of_Finance). He argued that participants' biased perceptions shape the situation they are perceiving, which in turn reshapes those perceptions.

### Homoiconicity

Homoiconicity makes the program a field of centers. Douglas Hofstadter coined the term in [*Gödel, Escher, Bach*](https://en.wikipedia.org/wiki/G%C3%B6del,_Escher,_Bach) for languages like Lisp, where code and data share one representation. Such a system observes its own structure and applies the same minimal, structure-preserving transformations to itself. Reflexivity becomes operational. The software regenerates its coherence from within. Every extension becomes living structure, not bolted-on matter.
