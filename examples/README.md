---
id: examples
type: example
status: active
last_reviewed: 2026-09-14
---

# Examples

Two halls. Both exist because examples displace the default register in a way adjectives never do.

**Hall of fame** (`hall-of-fame/`): replies and stories that show the standard. Some are synthetic, written to the house voice. Some are well-known public stories retold in our own words. Each one says why it works and which principles it embodies, because the why is what transfers.

**Hall of shame** (`hall-of-shame/`): failures, ours in principle and the industry's in fact. Each one names the principle it violated and rewrites the reply the way the best person on the floor would have sent it.

## The rule

Every hall-of-shame entry must have a matching case in `evals/cases/` that reproduces the failure and asserts the fix. A failure we can describe but can't test is a failure we'll repeat.

Every hall-of-fame entry should have a matching case eventually. When you add one, add the case or open an issue for it.

## Adding an entry

Frontmatter: `id`, `moment` (from `moments/README.md`), `source` (`synthetic` or `public-story`). Public stories are hedged where details are uncertain and never quote private individuals. Synthetic entries use the house cast: Dana, Marcus, Ana, Jordan, Priya, Sam, Acme, Northwind.
