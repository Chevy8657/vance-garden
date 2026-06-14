import sys
from timeline_api import TimelineAPI

def display_dashboard():
    api = TimelineAPI()
    events = api.get_all_events()
    
    # Typography/Color styling constants
    OBSIDIAN_BG     = "\033[48;5;232m"
    FOUNDRY_TEXT    = "\033[38;5;250m"
    GOLD_LEAF_AMBER = "\033[38;5;214m"
    VITRUVEO_TEAL   = "\033[38;5;44m"
    CRITICAL_RED    = "\033[38;5;196m"
    RESET           = "\033[0m"
    BOLD            = "\033[1m"
    
    print(f"{OBSIDIAN_BG}{VITRUVEO_TEAL}")
    print("X" + "═" * 88 + "X")
    print(f"║ {BOLD}NODE-ALPHA-001 // READ-ONLY OPERATOR CONSOLE // TIMELINE MONITOR{RESET}{OBSIDIAN_BG}{VITRUVEO_TEAL}      ║")
    print("X" + "═" * 88 + "X" + FOUNDRY_TEXT)
    
    if not events:
        print("  [!] No exported JSON telemetry artifacts discovered in the vault.")
        print(VITRUVEO_TEAL + "X" + "═" * 88 + "X" + RESET)
        return

    print(f"  {BOLD}{'TIMESTAMP (UTC)':<22} {'REPORT ID':<18} {'TYPE':<22} {'YIELD':<8} {'RISK':<6}{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
    print("  " + "─" * 86)
    
    for ev in events:
        risk = ev.get('risk_level', 'UNKNOWN')
        risk_color = CRITICAL_RED if risk == 'HIGH' else GOLD_LEAF_AMBER if risk == 'MEDIUM' else VITRUVEO_TEAL
        
        timestamp = ev.get('generated_at', 'N/A')[:19].replace('T', ' ')
        report_id = ev.get('report_id', 'N/A')
        a_type    = ev.get('assessment_type', 'N/A')[:20]
        eff_yield = f"{ev.get('efficiency_yield', 0.0)}%"
        
        print(f"  {timestamp:<22} {report_id:<18} {a_type:<22} {eff_yield:<8} {risk_color}{risk:<6}{RESET}{OBSIDIAN_BG}{FOUNDRY_TEXT}")
        print(f"  └── Summary: {ev.get('summary', 'No summary attached.')}")
        print("  " + "·" * 86)

    print(VITRUVEO_TEAL + "X" + "═" * 88 + "X" + RESET)

if __name__ == "__main__":
    display_dashboard()
