# Authority (template)

```yaml
standing_grants:
  credits:
    max_per_incident_usd: 0
    max_per_customer_per_quarter_usd: 0
    requires_reason: true
  gifts:
    max_per_gesture_usd: 0
    max_per_month_usd: 0
  pii_read:
    fields: [name, email, company, plan, timezone]
    everything_else: nudge
  send:
    channels_without_review: []   # e.g. [live-chat]
    channels_draft_only: [email, slack, sms]
  access_changes: nudge
  deletions: nudge
  external_sharing: nudge
disclosure:
  when_asked: always
  proactive: when_it_materially_matters   # or: always
```

Zero means nudge every time. Raise a number when you're ready to let the agent be kind without asking inside that bound.
