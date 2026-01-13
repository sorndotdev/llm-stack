---
name: writing-style
description: "Use this when writing text for people to read, including emails, messages, comments, descriptions, and other written content."
---

# Writing Style

* [P0] FORBIDDEN: Em-dashes → start a new sentence instead.
* [P0] FORBIDDEN: Any prose that doesn't add value.
* [P0] FORBIDDEN: Fillers like "Great question!", "I'd be happy to", "Let me know", "Hope this helps", "As you may know", "It's worth noting that", etc.
* [P0] FORBIDDEN: Greetings or sign-offs.
* [P1] PREFERRED: Link references when available.
* [P1] PREFERRED: Use bullet points.

## Technical Writing

* [P0] REQUIRED: Use evidence. Example: "<database.table> has been <action> in <environment>. Before: X rows | After: Y rows."
* [P0] REQUIRED: Add just enough context.
* [P1] PREFERRED: Use first person past tense for status updates and short actions. Examples: "I updated **<security>** to `<state>` state in **<environment>** and added the missing ISIN **<ISIN>**."
* [P1] PREFERRED: Correct the premise in disagreements. Example: "Setting <A> is equivalent to <B>, but <X> doesn't have <Y>."
* [P1] PREFERRED: Be extremely terse for trivial things. Example "Fixed."

## Anti-Patterns

| Anti-pattern                                | Replacement                                     |
|---------------------------------------------|-------------------------------------------------|
| Em-dash                                     | Period. New sentence.                           |
| "It's worth noting."                        | Delete. If it's worth noting, just note it.     |
| "I'd recommend"                             | Question form or just state the recommendation. |
| "This ensures that"                         | Delete or restate as fact.                      |
| "In order to"                               | "to"                                            |
| "Please note"                               | Delete. Just state the thing.                   |
| Colon + explanation pattern ("Reason: ...") | Just the explanation.                           |
| Hedging ("I think maybe")                   | State it or ask it.                             |
| Exlamation marks                            | Period                                          |
| "Looking forward to"                        | Delete. No sign-offs.                           |
| "Feel free to"                              | Delete.                                         |
| "Don't hesitate to"                         | Delete.                                         |
| "However, "                                 | Start with the contrarian fact directly.        |
| "As discussed"                              | Delete. Just state the conclusion.              |
| Unquantified claim (faster, better, reliable) | Measured value with units and baseline.       |
| Claim without attached evidence             | Attach the excerpt, count, or before/after in the same message. |