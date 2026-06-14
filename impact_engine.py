# impact_engine.py

def calculate_foundry_impact(volume: float, advisor_count: int, active_ipes_count: int) -> dict:
    """
    Computes real-time economic yield of the Foundry platform based on active 
    brokerage operational metrics derived directly from the ledger.
    """
    HOURLY_VALUE = 35.00
    FOUNDRY_INVESTMENT = 50400.00  # Annual enterprise licensing node cost
    
    # Base operational friction: 8 hours of baseline manual friction per advisor, per month
    base_monthly_friction_hours = advisor_count * 8
    
    # Deployed IPE efficiency multipliers
    efficiency_multipliers = {1: 0.25, 2: 0.45, 3: 0.60, 4: 0.75}
    efficiency_pct = efficiency_multipliers.get(active_ipes_count, 0.75 if active_ipes_count > 4 else 0.0)
    
    hours_returned_monthly = round(base_monthly_friction_hours * efficiency_pct)
    hours_returned_annually = hours_returned_monthly * 12
    
    # Calculate Full-Time Employee (FTE) reallocation equivalent
    fte_equivalent = round(hours_returned_monthly / 160, 1)
    
    # Operational savings from returned capacity
    operational_savings = hours_returned_annually * HOURLY_VALUE
    
    # Split Margin Leakage Protection: fractional lift based on volume optimization
    leakage_protection_yield = volume * (0.0004 * active_ipes_count) 
    
    annual_value_created = int(operational_savings + leakage_protection_yield)
    net_value_created = int(annual_value_created - FOUNDRY_INVESTMENT)
    
    return {
        "hours_returned_monthly": hours_returned_monthly,
        "hours_returned_annually": hours_returned_annually,
        "fte_equivalent": fte_equivalent,
        "annual_value_created": annual_value_created,
        "net_value_created": net_value_created,
        "active_ipes": active_ipes_count
    }
