#!/bin/bash

TOKEN="SovereignNodeSecret2026"

echo "🔒 Initializing SECURE V.A.N.C.E. Engine multi-user stream simulation..."
echo "----------------------------------------------------------------"

# Office 2: High Impact
curl -s -X POST http://127.0.0.1:8080/submit \
  -H "Content-Type: application/json" \
  -H "X-Node-Token: $TOKEN" \
  -d '{
    "office_name": "Foundry District Bravo",
    "office_status": "PROVISIONING",
    "readiness_score": 78,
    "annual_impact": 512000.0,
    "recommendation": "Infrastructure Hardware Upgrade Required",
    "notes": "Main electrical breaker requires a 400 AMP split."
  }'
echo "🔒 Certified Injection: Foundry District Bravo"

# Office 3: Micro Footprint
curl -s -X POST http://127.0.0.1:8080/submit \
  -H "Content-Type: application/json" \
  -H "X-Node-Token: $TOKEN" \
  -d '{
    "office_name": "Boutique Pod Zero",
    "office_status": "ONLINE",
    "readiness_score": 99,
    "annual_impact": 125000.0,
    "recommendation": "Deploy Node Stack Tier-1",
    "notes": "Fiber connection verified; local local-first sync complete."
  }'
echo "🔒 Certified Injection: Boutique Pod Zero"

echo "----------------------------------------------------------------"
echo "🎉 Secure pipeline stream complete. Querying live analysis..."
echo "----------------------------------------------------------------"

# Trigger the read-only dynamic calculation engine
curl -X POST http://127.0.0.1:8080/brief/generate
echo ""
