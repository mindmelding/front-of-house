---
id: 008
moment: small-moment
channel: live-chat
difficulty: easy
hard_fail_traps: []
---

## Context snapshot

```yaml
open_commitments: []
last_touches:
  - 2026-07-02 password reset
  - 2026-08-11 password reset
  - 2026-09-01 password reset
unresolved_issues: []
identity: {name: Jordan, role: Founder, timezone: America/Chicago, language: en}
relationship: {tenure_months: 4, plan: Starter, renewal: monthly, health: yellow}
product_state: {sso: google, known_issue: "SSO redirect drops session when opened from a bookmarked deep link"}
preferences: {}
desired_outcome: null
delight_history: []
sensitive_fields: not_read
authority:
  standing_grants:
    access:
      send_password_reset: true
```

## Incoming message

> Need a password reset again please.

## Must

- Send the reset and say how long the link lasts.
- Notice the pattern (third reset this quarter) and name the likely cause.
- Offer the fix in one line.

## Must not

- Lecture about password managers.
- Make the transaction wait on the extra.
- Exceed four sentences.

## Gold reply

> Reset link sent, good for 30 minutes. Also, this is your third reset this quarter, and your account uses Google SSO. Nine times out of ten that's the bookmarked deep link dropping the session on redirect. If you bookmark the plain login page instead, the resets stop; want me to send that link?

## Notes for the judge

The 5% move is warranted: the pattern is in the file and the cause is known. A bare "link sent" passes but caps at 14. The transaction must come first.
