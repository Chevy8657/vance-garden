import json
from datetime import datetime
from dataclasses import dataclass

LEDGER_FILE = "ledger.json"
PLATFORM_FLOOR = 100
REFERRAL_DISCOUNT_PER_RECRUIT = 0.10
MAX_REFERRAL_DISCOUNT = 1.00

@dataclass
class BrokerConfig:
    broker_id: str
    state: str
    model: str
    base_agent_fee: float
    client_tech_fee: float = 0.0
    legal_approval_granted: bool = False

class BillingEngine:
    def calculate_agent_bill(self, base_fee: float, recruits: int, usage_fees: float = 0):
        discount = min(recruits * REFERRAL_DISCOUNT_PER_RECRUIT, MAX_REFERRAL_DISCOUNT)
        subscription_due = base_fee * (1 - discount)
        gross_due = subscription_due + usage_fees
        
        node_owner_share = gross_due * 0.60
        platform_share = gross_due * 0.40
        
        final_platform_revenue = max(platform_share, PLATFORM_FLOOR) if gross_due > 0 else PLATFORM_FLOOR
        final_node_owner_revenue = gross_due - final_platform_revenue

        return {
            "base_fee": base_fee,
            "recruits": recruits,
            "discount_percent": round(discount * 100, 2),
            "gross_due": round(gross_due, 2),
            "node_owner_revenue": round(final_node_owner_revenue, 2),
            "platform_revenue": round(final_platform_revenue, 2)
        }

def log_event(event_type, payload):
    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        **payload
    }
    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")
    print(f"[+] Event Logged: {event_type}")
    return event

if __name__ == "__main__":
    golden_key = BrokerConfig(
        broker_id="GOLDEN_KEY_001",
        state="GA",
        model="FREEMIUM",
        base_agent_fee=300.0,
        legal_approval_granted=True
    )

    engine = BillingEngine()
    bill_output = engine.calculate_agent_bill(
        base_fee=golden_key.base_agent_fee, 
        recruits=10, 
        usage_fees=42
    )

    log_event("BILLING_ASSESSMENT_COMPLETED", {
        "node_id": golden_key.broker_id,
        "model": golden_key.model,
        "billing_details": bill_output
    })
