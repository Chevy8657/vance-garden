import os
import sys

sys.path.append(os.path.join(os.getcwd(), "foundry_property"))

try:
    from property_registry import PropertyRegistry
    print("[✓] PropertyRegistry import: PASS")

    registry = PropertyRegistry()
    print("[✓] PropertyRegistry init: PASS")

except Exception as e:
    print(f"[✕] PropertyRegistry check FAILED: {e}")
    raise SystemExit(1)

print("[★] STACK VERIFY: SUCCESS")
