import sys
import os
sys.path.append(os.path.join(os.getcwd(), "foundry_marketplace"))

from marketplace_dossier import MarketplaceDossier

exporter = MarketplaceDossier()
filepath, data = exporter.generate()

print(f"[✓] Dossier Exported: {filepath}")
print(f"[✓] Health Status: {data['marketplace_health_status']}")
print(f"[✓] Trust Posture: {data['executive_summary']['trust_posture']}")

assert os.path.exists(filepath)
assert data["dossier_type"] == "MARKETPLACE_TRUST_DOSSIER"
print("[★] MARKETPLACE DOSSIER EXPORT VERIFY: SUCCESS")
