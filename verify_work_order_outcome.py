import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from work_order_outcome import OutcomeEngine

engine = OutcomeEngine()

# Record an outcome where an override was utilized
outcome = engine.record_outcome(
    wo_id="WO-001",
    vendor_id="VEND-001",
    prop_id="PROP-001",
    used_override=True,
    status="SUCCESS",
    evidence="HASH-EVIDENCE-001"
)

print(f"[✓] Outcome Recorded: {outcome['outcome_id']}")
print(f"[✓] Risk Decision Justified: {outcome['outcome_status']}")

assert outcome["used_manager_override"] is True
assert outcome["outcome_status"] == "SUCCESS"

print("[★] WORK ORDER OUTCOME VERIFY: SUCCESS")
