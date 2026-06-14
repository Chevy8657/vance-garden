# agent_rollup.py
import json
import os

def run_agent_rollup(agent_ledger_path, brokerage_ledger_path, brokerage_name="Tracy Commercial Realty"):
    """
    Reads decentralized agent transaction lines, aggregates firm-wide telemetry,
    and writes the master entry directly into the brokerage ledger.
    """
    if not os.path.exists(agent_ledger_path):
        print(f"Error: {agent_ledger_path} not found.")
        return False

    total_volume = 0.0
    unique_agents = set()
    
    try:
        with open(agent_ledger_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                deal = json.loads(line.strip())
                
                # Roll up closed deals
                if deal.get("status") == "closed":
                    total_volume += float(deal.get("deal_volume", 0))
                    unique_agents.add(deal.get("agent_id"))
        
        # Calculate dynamic readiness based on volume depth
        calculated_readiness = min(50.0 + (len(unique_agents) * 5.0), 95.0)
        
        # Structure the rolled-up master entry
        master_entry = {
            "brokerage_name": brokerage_name,
            "annual_volume": f"{total_volume:,.2f}",
            "advisors": len(unique_agents) if unique_agents else 1,
            "ownership_readiness": f"{calculated_readiness}%"
        }
        
        # Append the calculated state cleanly to the master ledger
        with open(brokerage_ledger_path, "a") as f:
            f.write(json.dumps(master_entry) + "\n")
            
        print(f"SUCCESS: Rolled up {len(unique_agents)} agents. Total Volume: ${total_volume:,.2f}")
        return True

    except Exception as e:
        print(f"Rollup Engine Error: {str(e)}")
        return False

if __name__ == "__main__":
    AGENT_PATH = "/home/rick/pet_alpha/agent_ledger.json"
    BROKER_PATH = "/home/rick/pet_alpha/brokerage_ledger.json"
    run_agent_rollup(AGENT_PATH, BROKER_PATH)
