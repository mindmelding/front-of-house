# Who counts as a customer (local, filled in by the First Shift)

rule: <the operator's rule, e.g. "account stage is Onboarding, Active, or At Risk" or "on the paying list at <path>">
source of the rule: <operator said so | proposed heuristic, confirmed 2026-..-..>

## Heuristics (if no rule was given), most confident first
1. <e.g. paying plan in billing>
2. <e.g. account stage past prospect>
3. <e.g. sender domain not ours and not a known vendor>

## Unsure (ask before drafting to these)
- <account or domain>: <why unsure>

## Not customers (never draft a customer reply to these)
- vendors: <domains>
- investors, candidates, partners: <domains>
- teammates: <our domains>
