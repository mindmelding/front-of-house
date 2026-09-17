---
moment: feature-request
inherits: moments/feature-request/PLAYBOOK.md
confidence: low
evidence: 11
rules: 0
drills_run: 0
last_reinforced: 2026-09-17
---
# How we do feature request

Empty means: do what the canon says. Every line below is a divergence with evidence, a
confirmation date, and an expiry. Names are aliases (`engine.py alias`); this file can leave the building.

## Our policy

(from overlay/policies.md and overlay/authority.md, only what applies to this moment)

## Where we differ from the canon

- [2026-09-17] Ask one scoping question about the job before saying what the product can do: historical or forward-only, which two fields, how big the list. (UNCONFIRMED, source: Fjord 2026-08-18; Fjord 2026-08-27; Fjord 2026-09-01, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] When it is not native, say so in one line and offer a path we run ourselves (a Claude workflow or a hands-on build), tested on a small batch with results shared before the full run. (UNCONFIRMED, source: Fjord 2026-08-20; Fjord 2026-08-26; Fjord 2026-09-02, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Pre-pull the numbers before replying so the scope is concrete in the first message. (UNCONFIRMED, source: Fjord 2026-08-18; Fjord 2026-09-01, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Give a soft when for the next update (this afternoon, this week, right after Monday's call) and then post it on time, even if the answer is not ready. (UNCONFIRMED, source: Fjord 2026-08-29; Fjord 2026-09-01; Fjord 2026-09-08, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)

## What we actually sent (exemplars for this moment)

### 2026-09-17
> Slack thread, 2026-08-31 to 2026-09-02, to Avery, who asked (as "a shot in the dark") whether the product could fill in missing names and titles across their people records.
> 
> > I can pull an export if that's useful? Do you have the roles/titles in other tools?
> 
> > Let me take a look today and see what we can do! Were (1) Names and (2) Job Titles the key things you wanted to get refreshed?
> > Pulled the initial data yesterday and saw just around 14.3k folks with either no name or email, so those are the numbers we'd try to update if so!
> 
> > For this list, it looks like ~14k folks don't have a job title. I've distilled this down to around ~12k emails that are actually valid email addresses. While this is beyond the Agent functionality, my thinking is I can identify which of these actually are associated with an active LinkedIn, and we can pull job titles from there. Think that would work? I'll test with around 1k emails and can share those results to see if that looks good to you.
> 
> > Shared over a Google Sheet with the first group to see if that looks directionally correct

**Why it works:** Pre-pulled the numbers, scoped the ask to two fields, proposed a build beyond product scope, and tested on a small batch first.

### 2026-09-17
> Slack, 2026-08-27 to 2026-08-28, to Rowan, who asked how to email a whole list without approving each draft, and asked to be shown how so she would not need the operator every time:
> 
> > you can definitely do this without approving each draft. The Agent builds the audience, then our Email tool sends to the whole list at once.
> > Two things: how big is the list? And if you kick the file over to me, I'll handle the upload and audience build so you can jump straight to writing the email.
> 
> > On it! I'll prep this list for you and then show you how I did it for the next run. Will have this ready to roll early tomorrow morn

**Why it works:** Answers the how-do-I, asks one scoping question, takes the work this time and offers to teach on the next run.

### 2026-09-17
> Slack thread, 2026-08-18 to 2026-08-20, to Rowan, who asked for emails that fire when an account stops collecting data:
> 
> > Let me take a peek! Were you looking to run it for all historical accounts, or just any account hitting that condition moving forward?
> 
> > Got it! I'll put together a recommendation for this. Are you using Claude Code / Cowork currently?
> 
> > We don't have a great way to trigger based on conditions natively, but I actually think this may be a good Claude use case. I'll share some ideas to see what you think!
> 
> > Does Customer.io also have the same signals in the data you'd be looking for (e.g. not collecting data for X period of time)?

**Why it works:** Asks historical-versus-forward before anything else, says plainly that it is not native, and points at the nearest real path.

## Runbook

(written the second time this is done by hand; steps, what goes wrong, when to escalate instead)

## Drill record

## Counter-examples

(denied proposals; the engine never re-proposes these)
