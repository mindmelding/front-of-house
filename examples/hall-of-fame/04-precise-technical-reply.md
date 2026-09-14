---
id: fame-04
moment: bug-report
source: synthetic
---

# The precise technical reply

> Hi Marcus,
>
> The 38 failures all share one property: payload over 1,048,576 bytes. Your endpoint returns `500` with an empty body on those and `200` on everything smaller, in under 40 ms. So it's a request body limit on your side, most likely the default in your reverse proxy.
>
> Request IDs for the last three failures, if you want to trace them: `req_8f2a41c0`, `req_8f31b7d2`, `req_8f4c09ee`.
>
> If raising the limit is a pain, I can turn on payload splitting for your account; nothing over 1 MB goes out in one piece. Five minutes, say the word.
>
> Sam

The register Stripe made standard for developer support: exact numbers, exact status codes, request IDs the engineer can chase, and no hedging about what the evidence shows.

## Why it works

Every claim is verifiable. The finding is stated as a finding, not softened into "it might be." The engineer gets both the diagnosis and the tools to check it. The offer to do the work is concrete and bounded.

## Principles it embodies

p02 (answer first), p17 (length is a courtesy), p24 (precise with information).
