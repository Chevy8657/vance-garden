class HealthScorer:
    @staticmethod
    def calculate(dossier):
        score = 0
        
        # 1. Inspection Compliance
        if dossier.get("inspection_status") == "VERIFIED": score += 20
        
        # 2. Maintenance Compliance
        # Updated: Allow up to 1 open item without penalizing the full 25 points
        maint = dossier.get("maintenance_status", {})
        open_maint = maint.get("open", 0)
        if open_maint <= 1: 
            score += 25
        elif open_maint <= 3:
            score += 15
            
        # 3. Occupancy
        if dossier.get("occupancy_status") in ["OCCUPIED", "VACANT"]: score += 15
        
        # 4. Chain Integrity
        if dossier.get("chain_integrity") == "VERIFIED": score += 20
        
        # 5. Attestation
        if dossier.get("manager_attestation"): score += 20
        
        return {
            "score": score,
            "risk_classification": "LOW" if score > 85 else "MEDIUM" if score > 60 else "HIGH"
        }
