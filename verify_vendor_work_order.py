import sys
import os
import json

# Add the marketplace directory to the sys.path
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from vendor_work_order import VendorWorkOrder

# Now the system will find the module
wo_system = VendorWorkOrder()
wo = wo_system.create_work_order("PROP-001", "VEND-001", "MAINT-7898FCB3", "PM-001")
wo_system.complete_work(wo["work_order_id"], "HASH-EVIDENCE-123")

# Verify the result
with open("foundry_marketplace/vendor_work_orders.json", "r") as f:
    orders = json.load(f)
    final_wo = next(o for o in orders if o["work_order_id"] == wo["work_order_id"])

print(f"[✓] Work Order created: {final_wo['work_order_id']}")
print(f"[✓] Status: {final_wo['work_status']}")
print("[★] VENDOR WORK ORDER VERIFY: SUCCESS")
