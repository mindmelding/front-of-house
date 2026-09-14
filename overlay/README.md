# Overlay (yours, private, not in this repo)

The canon is company-agnostic on purpose. Everything specific to *your* company lives in an `overlay/` directory that you keep private and load after the canon:

```
overlay/
  README.md          who you are, what you sell, who your customers are (200 words)
  authority.md       standing grants: credits, gifts, PII fields, send authority (see guardrails/authority.md)
  policies.md        the written rules: refunds, SLAs, data retention, disclosure. If it isn't here, it isn't policy.
  product.md         what the product does, common issues, where things are
  people.md          who to escalate to for what, with timezones
  voice-overrides.md sign-offs, emoji policy, anything narrower than the canon voice
  exemplars.md       your own best replies, annotated
```

Load order: canon → overlay → context graph → conversation.

Rules:
- The overlay may **narrow** a guardrail. It may never loosen one.
- Anything not written in `policies.md` is not policy. The agent escalates.
- Until `authority.md` grants something, every sensitive action is a nudge.
- Keep real customer data out of both repos. The context graph holds it; the overlay describes how to reach it.

Templates for each file are in this directory.
