---
moment: migration-and-export
inherits: moments/migration-and-export/PLAYBOOK.md
confidence: low
evidence: 11
rules: 0
drills_run: 0
last_reinforced: 2026-09-17
---
# How we do migration and export

Empty means: do what the canon says. Every line below is a divergence with evidence, a
confirmation date, and an expiry. Names are aliases (`engine.py alias`); this file can leave the building.

## Our policy

- Data retention and export are unwritten policy (overlay/policies.md, 2026-09-15): never quote a retention window or deletion date; say we will confirm and by when, and escalate the number to the operator.
- Customer fields may be read freely (pii_read: all, First Shift 2026-09-15). Sending data to any address or system not already on the account is external sharing and nudges every time; deletions and access changes also nudge.
- Email and Slack are draft-only channels; every export message and every export file goes out by the operator's hand.
- Product context that applies: the traditional CRM/marketing product is being wound down with a year-end goal; the account's own people may receive their own data via API, CSV snapshot, or a direct push we run, and the workspace stays live and read-write until the customer says go (observed practice, Fjord 2026-09-08 and 2026-09-16; not yet written policy).

## Where we differ from the canon

- [2026-09-17] After every transition call, post a same-day recap in the shared channel with three owner-tagged action items (ours, theirs, together) and the next artifact attached, not promised. (UNCONFIRMED, source: Fjord 2026-09-08; Fjord 2026-09-16, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Give the API path first with exact endpoints and an upsert-by-stable-ID recipe, then offer the bundled CSV snapshot as the easier alternative in a second message, and say both land in the same place. (UNCONFIRMED, source: Fjord 2026-09-15; Fjord 2026-09-16, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Ship a small sample export for format approval before the full backup, and set the final snapshot date only after the customer's destination is decided. (UNCONFIRMED, source: Fjord 2026-09-16; Fjord 2026-09-02, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Offer to populate both candidate destinations with their data so they can compare side by side before choosing. (UNCONFIRMED, source: Fjord 2026-09-08; Fjord 2026-09-08, evidence: 2, reinforced: 2026-09-17, expires: 2026-12-16)
- [2026-09-17] Name the wind-down window and the year-end goal in the recap, and say we stay live and read-write until they say go. (UNCONFIRMED, source: Fjord 2026-09-08; Fjord 2026-09-16; Kestrel 2026-08-19, evidence: 3, reinforced: 2026-09-17, expires: 2026-12-16)

## What we actually sent (exemplars for this moment)

### 2026-09-17
> Slack, shared channel, 2026-09-16, same day as the 10am transition call, to Devon and Tatum:
> 
> > thanks again for today. As a quick recap, we covered the HubSpot/Attio evaluation and preserving account relationships and legacy affiliate data. We agreed to validate a small export before preparing the full backup.
> >
> > Action items
> > • Moonbase: Share the sample; prepare the full export after approval.
> > • Your team: Confirm the format, relationships, and any missing data.
> > • Together: Set the final snapshot date after the CRM decision; Moonbase will help with migration.
> >
> > Here's the first cut of an export: [link]. This includes a sample of representative records, schemas, relationship pointers, and recent activities. I'd recommend focusing on the CSVs just to get a sense of the structure. If this looks good, we can export all data and package that up for y'all.

**Why it works:** Same-day recap with owner-tagged action items, and the sample export attached instead of promised.

### 2026-09-17
> Slack thread, 2026-09-15, to Tatum, 24 minutes after she asked how to get everything into their warehouse before wind-down. Two messages, four minutes apart:
> 
> > Here's a starting point for pulling Moonbase data into Snowflake:
> > • Collections: Enumerate the workspace's collections (the overarching list and schemas) [Collections API]
> > • Items: Paginate through the records for each collection and merge on the Moonbase item ID [Items API]
> > • Meetings: List and paginate meeting records; preserve meeting IDs, timestamps, attendees, notes/transcript fields, and related record IDs [Meetings API]
> > On the Snowflake side, I'd recommend a scheduled job to call the API, land the responses, and upsert them by stable ID. Notes, meetings, and other activity should likely be scoped separately rather than assumed to be covered by these resources.
> 
> > If helpful, we can also export a bundled CSV snapshot of each Moonbase collection. This would be the equivalent of exporting CRM objects/tables like People, Organizations, Deals, and custom objects from HubSpot or Salesforce. Just in case that's easier to load into Snowflake vs. tying into the API. Should be the same outcome either way, but wanted to offer that just in case!

**Why it works:** API path with exact endpoints and an upsert recipe first, then the easier CSV path offered unprompted, both said to land in the same place.

### 2026-09-17
> Slack, shared channel, 2026-09-08, about an hour after the call where the wind-down was first explained, to Avery (written so she could carry it into her company-wide call that afternoon):
> 
> > Thanks again for the conversation today. A few follow-ups from our side:
> > • We're planning to wind down Moonbase's traditional CRM/marketing product over the next 2–3 months, with a goal of completing the transition before year-end. We'll be here to help with each step of that move.
> > • Based on our chat, Attio + Customer.io looks like the leading path, with HubSpot still a viable alternative. Let us know what your team thinks during the chats today and this week.
> > • I'll spend time this week reviewing your form-related use cases and workflows, then share that context to help the team choose the best next platform for forms.
> > Also, as a nudge, we're more than happy to help migrate data to both systems if the team wants to cross-compare them at any point. We'll be in touch, but feel free to reach out at any time with questions - we're around!

**Why it works:** Wind-down window and year-end goal named plainly, leading option stated, and an offer to populate both candidate systems for comparison.

## Runbook

(written the second time this is done by hand; steps, what goes wrong, when to escalate instead)

## Drill record

## Counter-examples

(denied proposals; the engine never re-proposes these)
