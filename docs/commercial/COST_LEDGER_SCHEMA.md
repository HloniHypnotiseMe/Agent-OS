# Cost Observation Schema

Each customer/pilot observation should capture:

```text
observation_id
customer_id
package_id
period_start
period_end
revenue_zar
llm_cost_zar
research_cost_zar
enrichment_cost_zar
email_cost_zar
hosting_cost_zar
payment_cost_zar
human_delivery_cost_zar
implementation_cost_zar
third_party_cost_zar
unknown_cost_zar
total_direct_cost_zar
gross_margin_zar
gross_margin_pct
confidence
source_refs
notes
```

`unknown_cost_zar` must be explicit. Missing cost data must never be coerced to zero.

## Acceptance criteria

- Every activated pilot can produce one observation per billing period.
- Total direct cost is reproducible from component costs.
- Gross margin is reproducible from revenue and total direct cost.
- P50/P90 package cost can be calculated from observations.
- Evidence/source references are retained for auditability.
