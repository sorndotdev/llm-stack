---
name: plant-uml
description: "Use this skill whenever you're generating with PlantUML diagrams"
---

## Workflow

1. Create the diagram using Syntax Rules below
2. Validate structurally
3. Render-verify: `java -Djava.awt.headless=true -jar <plantuml.jar> -checkonly <file>` before rendering (PlantUML renders broken files as broken PNGs (rc=200), so never trust a successful `-tpng` as proof of validity)
4. On error, fix the specific line and re-verify. Retry with the error text, never regenerate blindly
5. Keep diagrams small: 3-6 classes with direct relationships only.

## Syntax Rules

* Output only PlantUML between `@startuml`/`@enduml` - no prose, no triple backtick fences
* Declare every element BEFORE any arrow or note referencing it
* Fields `+name : Type`
* Methods `+name(Param) : Return`
* Inheritance `Parent <|-- Child`
* Realization `Interface <|.. Impl`
* Dependency `A ..> B`
* Association `A --> B`
* Stereotypes: `<<Entity>>`, `<<ValueObject>>`, `<<Aggregate>>`, etc.
* Notes: `note right of ClassName #LightCoral` ... `end note` HTML inside notes (`<b>`, `<code>`, `<br/>`) is valid - do NOT escape it to `~b~`
* Any bare `<` that isn't HTML in notes or `<<sterotype>>` breaks the parser. Examples:
  * `Optional<String>` MUST be `Optional~String~` (generics)
  * `Model<T1, T2>` MUST be `Model~T1+T2` (commas in generics)
  * `<note>`/`</note>` XML note tags are invalid, use `note`/`end note`
* Dots in name breaks the parser `class A.B {}` MUST be `class "A.B" as A_B` and reference `A_B` in all arrows and `note right of A_B`
* Unsupported Java keywords: `sealed`, `permits`
* Stereotype order: `class Foo <<S>> as "Name"` is invalid - `as` clause MUST come before the stereotype
* Newlines in quoted notes: `note "a\nb" as N1` fails - use `<br/>`
* Only one `#Color` in note is allowed
* `usecase` in class diagram causes allowmixing errors
* `skinparam style strictuml` causes rendering issues
* Tilde-corrupted arrows are never valid (no arrow terminates in `~`): `--~`, `..~`, `~|--`, `--|~`