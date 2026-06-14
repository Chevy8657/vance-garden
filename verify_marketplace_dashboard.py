import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from marketplace_dashboard import MarketplaceDashboard

dashboard = MarketplaceDashboard()
report = dashboard.get_health_report()

print("--- MARKETPLACE CONTROL TOWER ---")
for key, value in report.items():
    print(f"{key.replace('_', ' ').title()}: {value}")
print("---------------------------------")

assert "total_vendors" in report
assert report["health_status"] in ["STABLE", "ACTION_REQUIRED"]
print("[★] MARKETPLACE DASHBOARD VERIFY: SUCCESS")
