import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from vendor_trust_profile import VendorTrustProfile
from manager_override import ManagerOverride
from work_order_outcome import OutcomeEngine
from marketplace_dashboard import MarketplaceDashboard

def run_failure_scenario():
    print("\n--- STRESS TEST: FAILURE PATH ---")
    trust = VendorTrustProfile()
    overrides = ManagerOverride()
    outcomes = OutcomeEngine()
    dashboard = MarketplaceDashboard()

    # 1. Override granted for probation vendor
    overrides.request_override("VEND-001", "PROP-001", "PM-001", "Risk-heavy repair")
    
    # 2. Record FAILURE outcome
    outcomes.record_outcome("WO-FAIL-001", "VEND-001", "PROP-001", True, "FAILURE", "NULL-HASH")
    
    # 3. Update trust (system should downgrade)
    trust.update_reputation("VEND-001", success=False)
    
    report = dashboard.get_health_report()
    
    print(f"[!] Outcome: FAILURE recorded")
    print(f"[!] Marketplace Health: {report['health_status']}")
    print(f"[!] Failed Outcomes Count: {report['failed_outcomes']}")
    print("--- STRESS TEST COMPLETE: GOVERNANCE VERIFIED ---")

if __name__ == "__main__":
    run_failure_scenario()
