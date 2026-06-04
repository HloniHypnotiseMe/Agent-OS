"""
Agent-OS Workflows: Research to Executive Report

Example multi-agent workflow definition.
"""

WORKFLOW = {
    "name": "research_to_report",
    "description": "Research a topic, then have CEO synthesize into strategy, then marketer prepare go-to-market summary.",
    "steps": [
        {"agent": "researcher", "task": "Deep research on the topic", "depends_on": []},
        {"agent": "ceo", "task": "Synthesize research into strategic recommendations", "depends_on": ["researcher"]},
        {"agent": "marketer", "task": "Prepare messaging and campaign outline based on strategy", "depends_on": ["ceo"]}
    ]
}

def get_workflow():
    return WORKFLOW