# C6 Commercial Engine TODO

## Completed

- [x] Forensics across Agent-OS, C6 website and RemotePay
- [x] Product/package catalogue identified
- [x] Initial market pricing benchmark
- [x] Pricing decision logged
- [x] Unit-economics margin gates defined
- [x] Cost observation schema defined
- [x] Cost observation calculation and JSONL persistence implemented
- [x] Missing-cost guardrail implemented (`None` stays unknown; no silent zero)
- [x] Deterministic margin-gate helper implemented
- [x] P50/P90 package cost calculation implemented
- [x] Automated CI test gate added for the cost ledger
- [x] Provider-agnostic cost event schema/recorder implemented
- [x] Cost-event normalization and aggregation tests implemented
- [x] Actual AI/LLM usage events wired (Ollama)
- [x] Actual research/search usage events wired
- [x] Enrichment usage hook generated and tested
- [x] Email/outreach usage hook generated and tested
- [x] Enrichment hook wired into ResearcherAgent web-search execution
- [x] Outreach hook wired into SalesAgent send_outreach execution

## Current phase — COST LEDGER

- [x] Define direct-cost categories
- [x] Define package margin gates
- [x] Define customer cost observation schema
- [x] Define normalized provider cost-event contract
- [x] Implement cost-event validation and source attribution
- [x] Implement event aggregation into package observations
- [x] Wire actual AI/LLM usage events
- [x] Wire actual research/search usage events
- [x] Generate enrichment usage instrumentation boundary
- [x] Generate email/outreach usage instrumentation boundary
- [x] Wire enrichment hook into the real provider execution path
- [x] Wire outreach hook into the real provider execution path
- [ ] Wire actual hosting/runtime usage events
- [ ] Wire actual payment-cost events
- [ ] Wire actual human delivery/support time
- [ ] Wire actual implementation and third-party attributable costs
- [ ] Capture first 10 controlled observations
- [ ] Calculate P50/P90 package cost from real observations
- [ ] Validate package margins against gates

## Next phases

- [x] Discovery Intelligence v1
- [ ] Evidence/provenance graph hardening
- [ ] Opportunity detector hardening
- [ ] Offer engine hardening
- [ ] Canonical price resolver
- [ ] C6 → payment bridge
- [ ] Customer outcome tracking
- [ ] Learning/self-correction loop
- [ ] Economic Spine

## Operating rule

Do not change package prices because they feel too high or too low. Change them only when observed acquisition, delivery cost, conversion, retention, and margin evidence justifies the change.
