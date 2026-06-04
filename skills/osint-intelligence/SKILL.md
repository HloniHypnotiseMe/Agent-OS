# osint-intelligence Skill

## Description
Open-source intelligence gathering, people tracking, connection mapping, and investigation management (CRM-style).

## Inputs
- `target`: person/company name
- `depth`: "basic" | "deep"

## Execution
Uses Researcher + new OSINT tools. Stores in knowledge/projects.

## Core Logic
- Search public sources
- Build connection graphs
- Generate reports (inspired by GHOST)

## Dependencies
- research_skill
- web tools (MCP)
- projects/project_manager

## Integration
Enhances Legal, Researcher, and Business agents. Used for competitive intelligence and due diligence.

---
*Inspired by https://github.com/elm1nst3r/GHOST-osint-crm*
