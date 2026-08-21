# C6 Discovery Intelligence v1

## Goal

Turn a business URL into an evidence-backed commercial intelligence record and a machine-readable C6 offer, with a pure handoff contract for the existing RemotePay payment API.

## System map

| Stage | Existing capability | v1 role |
|---|---|---|
| Web research | `tools/web/web_search.py` | Source collection |
| Research orchestration | `agents/researcher/researcher.py` | Existing research pattern; v1 pipeline uses the same injected-tool boundary |
| Memory | Agent-OS memory layer | Available for later persistence; not required for deterministic v1 tests |
| C6 intelligence | `integrations/C6Group.AiOS` | Existing C6 intelligence subsystem; v1 emits a canonical record that can consume/extend it |
| Evidence | New `discovery_intelligence.models.Evidence` | Source, timestamp, confidence, verification status |
| Inference | New `discovery_intelligence.models.Inference` | Explicitly separated from source-backed facts |
| Opportunity | `DiscoveryIntelligencePipeline.score()` | Deterministic commercial opportunity score |
| Offer | `DiscoveryIntelligencePipeline.recommend()` | Maps opportunity to a C6 offer |
| Payment boundary | `RemotePayHandoff` | Maps offer to RemotePay `POST /payments` request shape |

## Canonical flow

```text
Business URL
  -> Agent-OS web research
  -> evidence[]
  -> business identity
  -> opportunity score
  -> recommendation
  -> C6 offer
  -> RemotePay payment request contract
  -> RemotePay transaction / PayFast
```

## Provenance rule

A source-backed fact is an `Evidence` record. A conclusion derived from evidence is an `Inference` record. They must never be represented as the same kind of object.

Every evidence item requires a source URL and a bounded confidence value. The record validator rejects factual identity fields that have no evidence coverage.

## RemotePay boundary

RemotePay currently exposes `POST /payments` with `amount` in cents, `currency`, `customer_id`, `return_url`, `cancel_url`, `item_name`, and optional `item_description`. It returns a transaction ID and checkout URL. The v1 handoff adapter intentionally does not perform network calls or own payment state; RemotePay remains the transaction owner.

## Current scope

- Build the contract and vertical slice in Agent-OS.
- Reuse existing web research infrastructure.
- Keep C6 Command Centre out of the critical path.
- Keep Ubernie as the separate discovery/customer experience workstream.
- Do not introduce dynamic pricing or a new payment implementation in this slice.

## Testable acceptance

1. A valid business URL produces a stable business identifier, evidence, inference, opportunity score, and offer.
2. Factual identity fields are provenance-validated.
3. The offer maps to the existing RemotePay `PaymentCreate` contract without provider credentials.
4. No test requires a live web request or live payment transaction.
