"""
Agent-OS: Autonomous CEO Loop (inspired by real deployment in C6Group.AiOS)

Runs the CEO agent on a schedule (every 15 minutes by default) for 24/7 autonomous operation.

Run in background on your server/laptop:
  python scripts/run_ceo_loop.py

This makes the "company" work while you sleep.
"""

import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import initialize_os

def run_autonomous_ceo(interval_minutes: int = 15):
    print("🚀 Starting Agent-OS Autonomous CEO Loop (24/7 mode)")
    print(f"   Will run CEO strategy cycles every {interval_minutes} minutes.")
    print("   Press Ctrl+C to stop.")
    
    components = initialize_os()
    ceo = components["agents"]["ceo"]
    
    cycle = 0
    while True:
        cycle += 1
        print(f"\n[Autonomous Cycle {cycle}] Running CEO strategic review...")
        try:
            strategy = ceo.set_strategy("Ongoing autonomous operations and opportunity detection for Agent-OS")
            print(f"   Strategy updated: {len(strategy.get('phases', []))} phases delegated.")
            
            # Optional: trigger a quick research
            researcher = components["agents"].get("researcher")
            if researcher:
                res = researcher.perform_research("Latest opportunities or threats for AI OS business")
                print(f"   Research completed and stored.")
        except Exception as e:
            print(f"   [Error in cycle] {e}")
        
        print(f"   Sleeping for {interval_minutes} minutes...")
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    run_autonomous_ceo()