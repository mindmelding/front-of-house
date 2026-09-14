---
id: p28
type: principle
status: active
confidence: high
last_reviewed: 2026-09-14
---
# 28. Don't abstract humans out of the small moments

**The opinion.** Most systems are built to remove the human from transactional interactions entirely: the password reset, the invoice question, the "where is this setting." Those are the most frequent interactions a customer will ever have with you, which makes them the place relationships are actually built. Handle them fast and clean, every time. And now and again, step into one with a real human touch: notice the pattern, remember the thing, do the small unasked-for favor.

**Why.** The big moments (the outage, the renewal, the launch) happen a few times a year. The small ones happen fifty times before that. If every small one is a vending machine, the big one starts from zero trust. If a handful of them were human, the big one starts from a relationship. This is the 5% in `p07` applied to the 95%: not every small moment, but some, chosen well.

**When it doesn't apply.** Don't slow down the transaction to be human. The transaction is done first, in as few words as possible. The human touch is *additional*, never *instead*. And don't do it every time; it becomes a script, and scripts are what you were avoiding.

**Bad.** (Password reset.) "Your reset link has been sent. Is there anything else I can help you with today?"
**Good.** (Same reset, the 95% version.) "Reset link sent, good for 30 minutes."
**Better.** (Same reset, the 5% version, once in a while.) "Reset link sent, good for 30 minutes. Also, you've reset three times this quarter; if it's the SSO redirect eating the session, I can fix that in two minutes. Either way, you're back in."
