# C6 Commercial Cost Ledger

**Status:** V1 control document
**Decision:** Package prices are controlled by the canonical catalogue; delivery cost must be measured before price changes.

## Margin gates

| Package | Current price | Target direct gross margin | Minimum acceptable |
|---|---:|---:|---:|
| Diamond | R4,995/mo | 70% | 65% |
| Gold | R9,995/mo | 75% | 70% |
| Platinum | R24,995/mo | 70% | 65% |
| Enterprise | Custom | 60%+ | 55% |

## Direct cost ledger

For every activated customer, record actual monthly direct delivery cost for:

- AI/LLM usage
- Web research/search usage
- Data enrichment
- Email/outreach infrastructure
- Hosting/runtime
- Payment processing
- Human delivery/support
- Customer-specific implementation
- Third-party SaaS/API costs directly attributable to delivery

Do **not** include general corporate overhead in direct gross-margin calculations.

## Measurement rule

For each package calculate:

`Direct Gross Margin % = (Revenue - Direct Delivery Cost) / Revenue * 100`

Track both **P50** and **P90** monthly direct delivery cost. Pricing is considered economically validated only after sufficient real or controlled pilot observations establish the P90 cost below the relevant margin gate.

## Guardrails

1. Discovery may recommend a package, but may not invent a price.
2. Offer construction must resolve price from the canonical product catalogue.
3. A package must not be sold below its approved minimum margin without an explicit commercial override.
4. Unknown costs are recorded as `UNKNOWN`, never silently treated as zero.
5. Inferred business intelligence must never be represented as verified fact.

## Next measurement target

Collect the first 10 controlled customer/pilot cost observations, then calculate package-level P50/P90 cost and margin. Use that evidence to determine whether the current price ladder should remain, increase, decrease, or be re-scoped.
