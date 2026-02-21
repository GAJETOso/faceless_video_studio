
import os
import sys
from main import FacelessVideoBot

def fast_demo():
    print("\n--- MATTERS OF VALUE STUDIO: ELITE LAUNCH SEQUENCE ---")
    bot = FacelessVideoBot()
    
    # 1. AI Content Strategy
    print("\n[1/3] INITIALIZING AI STRATEGY SESSION...")
    plan = bot.calendar.generate_weekly_plan()
    if plan:
        print("DONE: 7-Day Content Schedule Generated.")
        # Print a snippet of the plan
        for day in plan.get('days', [])[:3]:
            print(f"   - {day['day']}: {day['topic']} ({day['niche']})")
    else:
        print("Strategy session used fallback logic.")

    # 2. Viral Hook Design
    print("\n[2/3] DESIGNING HIGH-STAKES CGI VISUAL HOOK...")
    topic = "The Mystery of the Satoshi Nakamoto"
    hook_blueprint = bot.intro_engine.generate_cgi_hook(topic)
    print(f"DONE: Hook Optimized for Demographic Retention:")
    print(f"   Blueprint: {hook_blueprint[:150]}...")

    # 3. Niche Discovery & Opportunity Scan
    print("\n[3/3] SCANNING WORLD PULSE FOR BREAKING NEWS...")
    trending = bot.get_trending_opportunities()
    if trending:
        top = trending[0]
        print(f"DONE: Breakout Opportunity Found: '{top['title']}'")
        print(f"   Urgency: {top['urgency']} | Niche: {top['niche']}")
    
    print("\n--- DEMO COMPLETE: SYSTEMS FULLY OPERATIONAL ---")
    print("Next suggested action: Run 'python api.py' to explore via your web dashboard.")

if __name__ == "__main__":
    fast_demo()
