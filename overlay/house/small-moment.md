---
moment: small-moment
inherits: moments/small-moment/PLAYBOOK.md
confidence: low
evidence: 23
rules: 0
drills_run: 0
last_reinforced: 2026-09-17
---
# How we do small moment

Empty means: do what the canon says. Every line below is a divergence with evidence, a
confirmation date, and an expiry. Names are aliases (`engine.py alias`); this file can leave the building.

## Our policy

(from overlay/policies.md and overlay/authority.md, only what applies to this moment)

## Where we differ from the canon

- [2026-09-17] Ack in one line ('On it!', 'Will take care of that today!'), do the thing, then post a done line with a link where they can verify it themselves. (UNCONFIRMED, source: Fjord 2026-08-18; Fjord 2026-08-28; Fjord 2026-08-31; Fjord 2026-09-08; Fjord 2026-09-09; Fjord 2026-09-10, evidence: 8, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Before any bulk send, send a test, wait for the go, and state the exact send time in Pacific; after the send, post the tracking link and the open rate once it exists. (UNCONFIRMED, source: Fjord 2026-08-18; Fjord 2026-08-19; Fjord 2026-08-24; Fjord 2026-08-25; Fjord 2026-08-28; Fjord 2026-08-31; Fjord 2026-09-10, evidence: 7, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] When a request hits a product constraint, explain the constraint in one sentence and put the workaround in the same message. (UNCONFIRMED, source: Fjord 2026-08-28; Fjord 2026-08-31, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Hand the timing choice back to the customer ('what time should I fire this out?', 'if that feels too late I can push it to tomorrow') instead of deciding for them. (UNCONFIRMED, source: Fjord 2026-08-19; Fjord 2026-08-28; Fjord 2026-08-31, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Close each hands-on build with a count of what changed and an invitation to check it ('around 5.5k records updated', 'shout if anything looks off'). (UNCONFIRMED, source: Fjord 2026-08-26; Fjord 2026-09-08; Fjord 2026-09-11, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)

## What we actually sent (exemplars for this moment)

### 2026-09-17
> Slack, 2026-08-31, to Avery, before a scheduled campaign send:
> 
> > I'm planning to send Email 2 for the outreach around 10:30am PT today, after Rowan's email goes out.
> > I'll switch the marketing profile and reply-to back first so the replies route correctly for your email. If that ends up feeling too late, I can push it to first thing tomorrow morning instead - let me know what you prefer!
> 
> Then, after the send:
> 
> > Email 2 is sent! Metrics here: [link]

**Why it works:** Exact send time in Pacific, the sequencing reason, and the choice handed back to the customer; then the done line with the metrics link.

### 2026-09-17
> Slack, 2026-09-08, to Avery, who asked for a newly referred brand to be associated with its agency in the affiliate program. Two messages, sixteen minutes apart:
> 
> > Yes! Will update this morning.
> 
> > All set and associated as a referral. Take a look when you have a sec and shout if anything looks off!
> 
> Same shape on 2026-08-28 ("Absolutely! Let me get that set up for you. Should be just a few minutes" / "OK, they're all set and associated as a referral") and 2026-08-31.

**Why it works:** One-line ack, the change made in minutes, then a done line inviting them to verify.

### 2026-09-17
> Slack thread, 2026-08-28, to Rowan, who wanted the bulk email to come from her and asked to wait until Monday:
> 
> > Can absolutely send on Monday! For these bulk emails, we have to send from the marketing profile that was set up (and include an unsub link), but we could set you as the Reply To? And then also fine-tune some of the profile to make it feel more from you. Replies would go to you.
> 
> > perf! want me to queue this up for Monday at 6am PT?
> 
> > all set and scheduled! you can monitor that specific email [here].

**Why it works:** The product constraint explained in one sentence with the workaround in the same message, then the schedule confirmed and a monitoring link.

## Runbook

(written the second time this is done by hand; steps, what goes wrong, when to escalate instead)

## Drill record

## Counter-examples

(denied proposals; the engine never re-proposes these)
