---
name: writing-style
description: "Use this when writing text for people to read, including emails, messages, comments, descriptions, and other written content."
---

# Writing Style

* Don't use em dashes. Start a new sentence instead.
* Don't write prose that doesn't add value.
* Don't use fillers like "Great question!", "I'd be happy to", "Let me know", "Hope this helps", "As you may know", "It's worth noting that", etc.
* Don't include greetings or sign-offs.
* Link references when available.
* Use bullet points.

## Technical Writing

* Content must be digestible in a single pass by both humans and LLMs: conclusion first, one idea per sentence, lists over paragraphs, structure carried by headings and line breaks rather than connectors.
* Use evidence. Example: "<database.table> has been <action> in <environment>. Before: X rows | After: Y rows."
* Add just enough context.
* Use first person past tense for status updates and short actions. Examples: "I updated **<security>** to `<state>` state in **<environment>** and added the missing ISIN **<ISIN>**."
* Correct the premise in disagreements. Example: "Setting <A> is equivalent to <B>, but <X> doesn't have <Y>."
* Be extremely terse for trivial things. Example "Fixed."

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