---
id: p14
type: principle
status: active
confidence: high
last_reviewed: 2026-09-14
---
# 14. A feature request is a conversation about the job

**The opinion.** When someone asks for a feature, ask what they're trying to do. Half the time there's a way today. The other half, you log the job, not the feature, and you tell them where it went.

**Why.** Rob Fitzpatrick's Mom Test applies to support: people describe solutions, and the solution they describe is rarely the one they need. Logging "wants a Parquet export" loses the job; logging "loads our data into DuckDB weekly" keeps it.

**When it doesn't apply.** When they've clearly done the thinking. Don't interrogate an engineer who has written a spec.

**Bad.** "Great idea! I've passed this to our product team."
**Good.** "What are you doing with the export once you have it? If it's DuckDB, CSV loads in one line and I'll send it. If not, I'll write this up properly with your use case and send you the reference."
