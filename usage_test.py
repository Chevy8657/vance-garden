import json
from datetime import datetime

LEDGER_FILE = "/home/rick/pet_alpha/ledger.json"

class UsageEngine:
    def calculate_usage(self, agent_id: str, usage_type: str, units: int, unit_price: float):
        total_usage_fee = round(units * unit_price, 2)
        return {
            "agent_id": agent_id,
            "usage_type": usage_type,
            "units": units,
            "unit_price": unit_price,
            "total_usage_fee": total_usage_fee
        }

def log_event(event_type, payload):
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **payload
    }
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[+] Usage Signal Verified: {event_type} | Agent: {payload['agent_id']} | Total: ${payload['total_usage_fee']}")
    return event

if __name__ == "__main__":
    engine = UsageEngine()
    
    # Process 12 units of CONTRACT_AUDIT at $1.00 each
    result = engine.calculate_usage(
        agent_id="AGENT_001",
        usage_type="CONTRACT_AUDIT",
        units=12,
        unit_price=1.0
    )

    log_event("USAGE_FEE_CALCULATED", result)
