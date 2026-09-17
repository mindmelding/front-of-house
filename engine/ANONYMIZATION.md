---
id: engine-anonymization
type: guardrail
status: active
confidence: high
last_reviewed: 2026-09-17
---

# Anonymization: what you learn can leave; what you do stays

The engine writes two kinds of files and treats them differently.

| Kind | Files | Names | Leaves the overlay? |
|---|---|---|---|
| **Operational** (what the engine does) | `in-motion.md`, `briefs/`, `drafts/`, `ledger.json`, `directives.md`, `accounts/*/state.md`, `who.md`, `people.md`, `customers.md` | real | never |
| **Learning** (what the engine learned) | `house/`, `journal/`, `queue/`, `drills/`, `evals/`, `lexicon.md`, `method.md` | aliases only | may: publish, compare, upstream |

## How aliasing works

`overlay/private/aliases.json` maps real names to stable aliases. Accounts become one-word names from a fixed list (Alder, Basalt, Cobalt, and so on). People become first names (Avery, Blake, Casey, and so on); a registered full name also maps its first name when that first name is unambiguous, so "Holly said yes" and "Holly Beingessner said yes" alias the same way. Domains become `<word>.example`. The map is assigned in order of first sight, so the same real name always gets the same alias, and a house file stays readable across months.

Every `engine.py` command that writes a learning file passes its text through `anonymize()`: registered names are replaced longest-first with word boundaries, then emails, phone numbers, and record links (`/id/`, `/identity/`, `/org/`, `/people/`) are scrubbed. `engine.py alias apply` does the same for any text you want to paste somewhere shareable. `engine.py alias reveal` reverses it on screen for the operator, whose own screen is not a learning file.

## The gate

```
python3 scripts/engine.py alias audit
```

Scans every learning file for any registered real name and any email address. Exit 1 on a hit. The sweep runs it before closing; the refresh runs it before anything goes upstream; `make check` can run it too. `--fix` rewrites in place.

## The rule the audit cannot enforce

The audit only knows the names you registered. **Register before you write.** The sweep and prime specs both say: `alias add` every account and person you touch, before deriving anything from them. A name that never got registered will pass the audit and still be a leak. When in doubt, register it.

What the anonymizer does not attempt: rewriting a story so specific that the account is identifiable without its name ("the only customer migrating to a Snowflake warehouse this quarter"). The rule for house files is the same as for the inbox: the lesson, not the story. Keep the shape, drop the particulars.

## What never goes in a learning file, aliased or not

The customer's message verbatim (the operator's edit is the signal, not the customer's words). Billing details. Health scores quoted. Anything from context contract row 10. Internal nicknames. Anything the operator marked as not for the file.
