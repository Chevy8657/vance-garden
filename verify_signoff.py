import sys
import os
import json
sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

from manager_signoff import ManagerSignOff
from unified_dossier import UnifiedDossier

signoff = ManagerSignOff()
aggregator = UnifiedDossier()

# Perform Sign-off
signoff.attest("PROP-001", "RM-001", "Reviewed and verified.", "HASH-999")

# Verify Dossier inclusion
dossier = aggregator.generate("PROP-001")
print(json.dumps(dossier, indent=4))

assert dossier["manager_attestation"]["status"] == "CLOSED_ATTESTED"
print("[★] MANAGER ATTESTATION VERIFY: SUCCESS")
