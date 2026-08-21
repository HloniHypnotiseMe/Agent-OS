# Agent-OS Upgrade Log

## Commercial Engine — 2026-08-21 execution log

### Decision
Approved to generate missing cost instrumentation rather than wait for provider integrations that are not yet present in Agent-OS.

### Implemented
- Added `commercial/usage_hooks.py` with standardized enrichment and email/outreach telemetry boundaries.
- Added `tests/test_usage_hooks.py` covering both hooks, JSONL persistence, units, and the missing-cost rule.
- Updated `docs/commercial/TODO.md` to distinguish generated instrumentation from real provider wiring.
- Wired `ResearcherAgent.perform_research()` to emit an enrichment usage event after each successful web-search result.
- Wired `SalesAgent.send_outreach()` to emit an outreach usage event after successful `send_email` execution.
- Added `tests/test_commercial_delivery_instrumentation.py` covering both real agent execution paths with controlled fake providers.

### Important accounting rule
The hooks record usage immediately, but **do not invent monetary cost**. `cost_zar` remains unknown (`None`) until a real provider exposes or supplies an attributable cost. This preserves the existing margin-accounting rule and prevents false economics.

### Current status
- Enrichment instrumentation boundary: COMPLETE
- Outreach instrumentation boundary: COMPLETE
- Research execution wiring: COMPLETE
- Outreach execution wiring: COMPLETE
- Real external provider cost attribution: PENDING
- First 10 controlled observations: PENDING
- P50/P90 from observed package costs: PENDING
- Margin validation: PENDING

### Why this decision
The repository already has a provider-agnostic usage contract and JSONL sink. The missing capability was the explicit commercial capability boundary for enrichment and outreach. Creating the boundary first, then wiring it into the existing Researcher and Sales execution points, lets the economics ledger observe real execution without inventing provider pricing.

### Evidence boundary
Research currently uses the existing `web_search` tool and records one enrichment event per returned external result. Sales now has an explicit `send_outreach()` execution path that requires a configured `send_email` tool and records usage only after that call returns successfully. No external provider cost is assumed.

### Next execution target
Run the repository test suite on `feat/commercial-cost-instrumentation`. Then connect the `send_email` tool to the real deliverability provider when available and collect the first 10 controlled observations. Do not mark cost attribution or pricing validation complete until observed provider costs exist.

---

# Historical Agent-OS Upgrade Log

**Date of Analysis & Updates:** 2026-06-04 (continuing from previous session)

**Repos Analyzed (11 GitHub repositories):**
1. https://github.com/googleapis/mcp-toolbox (MCP Toolbox for Databases - tool calling standard)
2. https://github.com/kaymen99/personal-ai-assistant (Hierarchical multi-agent personal assistant with messaging integrations)
3. https://github.com/supertone-inc/supertonic (On-device multilingual TTS via ONNX)
4. https://github.com/tuneeai/free-music-generator (Text-to-music generation skill)
5. https://github.com/Shubhamsaboo/awesome-llm-apps (Curated collection of 100+ runnable LLM agent & RAG apps + skills)
6. https://github.com/wuyoscar/GPT-Image2-Skill (GPT Image generation/editing as agent skill with prompt gallery)
7. https://github.com/elm1nst3r/GHOST-osint-crm (OSINT investigation/CRM platform with .agents/skills structure)
8. https://github.com/runtipi/runtipi (Self-hosted homeserver app manager - one-click installs)
9. https://github.com/ferdinandobons/startup-skill (Specialized agent skills for startup validation, competitors, positioning, pitch)
10. https://github.com/mattpocock/skills (Composable "Skills for Real Engineers" - engineering-focused agent patterns)
11. https://github.com/MaxMiksa/Auto-Company (Autonomous 24/7 AI company with agents, workflows, dashboard, projects)

## Historical summary
The existing Agent-OS architecture adopted modular skills, hierarchical agents, research/OSINT patterns, MCP-style tooling, autonomous workflows, persistent memory, business/startup capabilities, deployment concepts, and multi-device interfaces. These historical changes remain below for provenance.

## Historical impact
Agent-OS retained a Python-first architecture and avoided copying whole external repositories. The commercial engine now builds on these existing foundations while adding explicit cost attribution and evidence-driven pricing controls.
