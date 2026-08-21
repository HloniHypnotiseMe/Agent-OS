# C6 Commercial Decision Log

## 2026-08-21 — Cost instrumentation

**Decision:** Move from the approved cost-ledger schema into code-level cost observation instrumentation before changing package prices.

**Why:** The canonical ledger requires actual direct delivery cost evidence and P50/P90 validation before pricing changes. The schema already requires reproducible totals, reproducible gross margin, percentile calculation, and retained evidence/source references.

**Implemented:**
- `commercial/cost_ledger.py` — observation model, validation, derived economics, JSONL persistence, P50/P90, margin gate.
- `tests/test_cost_ledger.py` — deterministic coverage for totals, missing-cost protection, percentiles, and margin gates.
- `.github/workflows/commercial-cost-ledger-tests.yml` — CI gate for the instrumentation.
- `commercial/cost_events.py` — provider-agnostic normalized cost-event contract, validation, source attribution and aggregation.
- `tests/test_cost_events.py` — event normalization, unknown-cost protection, aggregation and cross-customer isolation tests.

**Guardrail:** Missing cost data remains explicitly unknown. It is never silently converted to zero, and validated margin cannot be calculated while required cost inputs are missing.

**Not changed:** Package prices, Command Centre, Ubernie, RemotePay implementation, or the canonical catalogue.

**Next measurable gate:** wire real AI/LLM, research, enrichment, email, hosting, payment and human-delivery cost events; then collect the first 10 controlled customer/pilot observations. Only then re-evaluate P50/P90 economics and pricing.
