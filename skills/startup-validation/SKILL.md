# startup-validation Skill

## Description
Comprehensive startup validation, competitive intelligence, positioning, and pitch preparation for Agent-OS business layer.

## Inputs
- `idea`: string - The startup idea or problem
- `market`: string - Target market description (optional)
- `depth`: "quick" | "deep"

## Execution
Used by CEO, JARVIS, or dedicated Startup Validator agent. Chains research → competitors → positioning → pitch.

## Core Logic
1. Validate problem/solution (Onliness Test, research gate)
2. Competitive analysis + battle cards
3. Positioning derivation (5+1 framework)
4. Pitch deck elements ordering

## Prompts / Reasoning Cues
(Deep reasoning for new models like Opus 4.7)
- At synthesis points: "Deliberately reason step-by-step about uniqueness and defensibility before writing."
- At go/no-go gates: "Weigh evidence rigorously. Only proceed if clear signal exists."

## Examples
- Input: "AI OS for autonomous agents" → Full validation report, competitors list, positioning statement, pitch outline.

## Dependencies
- research_skill
- designer (for pitch visuals)
- web_search (MCP tools)

## Integration
Registered in business/startup/ and callable from JARVIS/CEO.

---
*Directly inspired by https://github.com/ferdinandobons/startup-skill and https://github.com/MaxMiksa/Auto-Company*
