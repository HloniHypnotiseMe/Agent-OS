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

## Current phase — COST LEDGER

- [x] Define direct-cost categories
- [x] Define package margin gates
- [x] Define customer cost observation schema
- [ ] Instrument actual AI/LLM usage
- [ ] Instrument research/search usage
- [ ] Instrument enrichment usage
- [ ] Instrument email/outreach usage
- [ ] Instrument hosting/runtime usage
- [ ] Instrument payment costs
- [ ] Instrument human delivery/support time
- [ ] Instrument implementation and third-party attributable costs
- [ ] Capture first 10 controlled observations
- [ ] Calculate P50/P90 cost per package from real observations
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
