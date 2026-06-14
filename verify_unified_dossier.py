import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from unified_dossier import UnifiedDossier

aggregator = UnifiedDossier()
dossier = aggregator.generate("PROP-001")

print(json.dumps(dossier, indent=4))
assert dossier["property_id"] == "PROP-001"
print("[★] UNIFIED DOSSIER VERIFY: SUCCESS")
