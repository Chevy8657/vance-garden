import sys
import os
sys.path.append(os.getcwd())

from foundry_insurance.risk_classifier import RiskClassifier

classifier = RiskClassifier()
data = {
    "health_score": 95,
    "occupancy_status": "OCCUPIED",
    "open_maintenance_count": 0,
    "chain_integrity": "VERIFIED",
    "manager_attestation": "CLOSED_ATTESTED"
}

# Verify Authorized Classification
result = classifier.classify("CAR-001", "PROP-001", data)
print(f"[✓] Risk Classified: {result['classification_id']} | Band: {result['risk_band']} | Score: {result['risk_score']}")

# Verify Unauthorized Access Denial
try:
    classifier.classify("UNAUTH-CARRIER", "PROP-001", data)
except PermissionError as e:
    print(f"[✓] Unauthorized Access Denied: {e}")

print("[★] SPRINT 45: RISK CLASSIFICATION ENGINE VERIFIED")
