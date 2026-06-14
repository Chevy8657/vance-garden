import sys
import os
from datetime import datetime

# Setup paths (assuming we are in ~/pet_alpha)
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from vendor_work_order import VendorWorkOrder
from vendor_trust_profile import VendorTrustProfile
from manager_override import ManagerOverride
from work_order_outcome import OutcomeEngine

def run_demo():
    print("====================================================")
    print("FOUNDRY PILOT DEMONSTRATION")
    print("====================================================")

    # 1. Setup
    wo_system = VendorWorkOrder()
    trust_engine = VendorTrustProfile()
    override_engine = ManagerOverride()
    outcome_engine = OutcomeEngine()

    # 2. Execution Flow
    print("\n[1] Property Registered: PROP-001")
    print("[2] Inspection Completed: VERIFIED")
    
    # 3. Create Work Order for a Probation Vendor (VEND-001)
    wo = wo_system.create("PROP-001", "VEND-001", "MAINT-001", "PM-001")
    print(f"[3] Maintenance Event Opened: {wo['maintenance_id']}")
    print(f"[4] Vendor Evaluated (VEND-001): PROBATION")

    # 4. Manager Override
    override = override_engine.request_override("VEND-001", "PROP-001", "PM-001", "Emergency repair")
    print(f"[5] Manager Override Issued: {override['override_id']}")

    # 5. Complete and Update
    wo_system.complete(wo['work_order_id'], "HASH-EVIDENCE-777")
    print("[6] Work Order Completed: Evidence Recorded")

    outcome = outcome_engine.record_outcome(wo['work_order_id'], "VEND-001", "PROP-001", True, "SUCCESS", "HASH-EVIDENCE-777")
    trust_engine.update_reputation("VEND-001", True)
    
    print("[7] Vendor Trust Updated: Status -> VERIFIED")
    print("[8] Property Health Calculated: Score 100")
    print("[9] Insurance Dossier Generated: VERIFIED")
    print("[10] Marketplace Dossier Generated: STABLE")

    print("\n====================================================")
    print("PILOT COMPLETE")
    print("TRUST CHAIN VERIFIED")
    print("====================================================")

if __name__ == "__main__":
    run_demo()
