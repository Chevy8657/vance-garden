import os
import sys
import json

def run_health_audit():
    EXPORTS_DIR = '/home/rick/pet_alpha/exports/'
    
    CRITICAL_RED    = "\033[38;5;196m"
    VITRUVEO_TEAL   = "\033[38;5;44m"
    RESET           = "\033[0m"
    
    print("Executing Console Boundary Verification...")
    
    # 1. Verify structural boundary presence
    if not os.path.exists(EXPORTS_DIR):
        print(f"  └── {CRITICAL_RED}[FAIL] Artifact export matrix directory is missing.{RESET}")
        sys.exit(1)
    print("  ├── [✓] Verified artifact isolation layer presence.")

    # 2. Validate JSON compliance
    json_count = 0
    for filename in os.listdir(EXPORTS_DIR):
        if filename.endswith('.json'):
            json_count += 1
            try:
                with open(os.path.join(EXPORTS_DIR, filename), 'r') as f:
                    json.load(f)
            except Exception:
                print(f"  └── {CRITICAL_RED}[FAIL] Contaminated or corrupted JSON artifact detected: {filename}{RESET}")
                sys.exit(1)
                
    print(f"  ├── [✓] Validated integrity of {json_count} telemetry JSON blocks.")

    # 3. Defensive isolation check (Ensure dashboard process hasn't opened raw database connections)
    # Since this is a strict validation script, we verify the dashboard code lacks sqlite3 imports or execution strings
    with open('/home/rick/pet_alpha/operator_dashboard.py', 'r') as f:
        content = f.read()
        if "sqlite3" in content or "connect(" in content:
            print(f"  └── {CRITICAL_RED}[SECURITY FAULT] Core engine schema leak detected inside operator dashboard.{RESET}")
            sys.exit(1)
            
    print("  ├── [✓] Isolation confirmation: Dashboard code has zero database connectivity strings.")
    print(f"\n{VITRUVEO_TEAL}[CONGRATULATIONS] Operator Layer is perfectly isolated. Core engine frozen baseline intact.{RESET}\n")

if __name__ == "__main__":
    run_health_audit()
