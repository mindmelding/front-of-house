---
moment: bug-report
inherits: moments/bug-report/PLAYBOOK.md
confidence: low
evidence: 7
rules: 0
drills_run: 0
last_reinforced: 2026-09-17
---
# How we do bug report

Empty means: do what the canon says. Every line below is a divergence with evidence, a
confirmation date, and an expiry. Names are aliases (`engine.py alias`); this file can leave the building.

## Our policy

(from overlay/policies.md and overlay/authority.md, only what applies to this moment)

## Where we differ from the canon

- [2026-09-17] Acknowledge within minutes ('Taking a look!'), then ask for only the one thing you cannot see yourself and say you already have a hunch. (UNCONFIRMED, source: Fjord 2026-08-19; Fjord 2026-08-26; Fjord 2026-08-31, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] While digging, give a temp fix or a check the customer can run, and keep every update in their thread until the longer-term fix is named. (UNCONFIRMED, source: Fjord 2026-08-19; Fjord 2026-08-31, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Say 'not sure why yet' and name the two possible causes rather than guessing at one. (UNCONFIRMED, source: Fjord 2026-08-19; Fjord 2026-08-26, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)

## What we actually sent (exemplars for this moment)

### 2026-09-17
> Slack thread, 2026-08-31, to Avery, who could not get the connector to work from her assistant. First reply two minutes after her report; resolved within the hour.
> 
> > Could you shoot over a screenshot of the error you're seeing in Cowork when you're trying to connect to Moonbase? I have a hunch on what's happening, but would be good to take a look
> 
> > Thanks! While I dig in, can you try running that Moonbase Connect skill (you can just ask Claude to run it) and then grab a key here: [settings link]
> > See if that works as a temp fix
> 
> > excellent! keep me posted if you run into it again

**Why it works:** Two-minute ack, asks only for the screenshot, admits a hunch, gives a temp fix while digging, closes with the door open.

### 2026-09-17
> Slack thread, 2026-08-19, to Avery, after she reported that a prospect's replies to a campaign were not showing up. Three messages over the day, all kept in her thread:
> 
> > Taking a look!
> 
> > Still digging into this, but will report back shortly on what we find + the longer term fix. I'll keep you posted in this thread.
> 
> > Do you see this reply in Moonbase, or is it in your Gmail?
> 
> > Got it! Not sure why they didn't sync back, but I'll take a peek into it

**Why it works:** Says 'not sure why' instead of guessing, promises the longer-term fix, and keeps every update in the customer's thread.

### 2026-09-17
> Slack, 2026-08-26, to Avery and Tatum, when a newly signed brand was missing from the affiliate view:
> 
> > Can take a look. Do you know the domain for the brand?
> 
> > Got it, thanks! I see them as an Organization, but not yet as an Account. Right now, we have the Source (e.g. referral source) on the Account. @Tatum Are you showing the account on the Snowflake table? Wondering if it's a sync issue, or if the Account might be under a different name
> 
> > ya, would expect if they're in that snowflake table, we'd see them pulled in. for context, once we do see them, we should be able to match/map if that source points to the agency. i'll take a peek as soon as we debug the account issue.

**Why it works:** States exactly what is seen in the data, names the two possible causes, and pulls in the customer's data owner with one specific question.

## Runbook

(written the second time this is done by hand; steps, what goes wrong, when to escalate instead)

## Drill record

## Counter-examples

(denied proposals; the engine never re-proposes these)
