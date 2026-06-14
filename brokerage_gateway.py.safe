import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from brokerage_brief import generate_brokerage_analysis

app = FastAPI()
BROKERAGE_LEDGER = "/home/rick/pet_alpha/brokerage_ledger.json"

def get_latest_brokerage_record():
    if not os.path.exists(BROKERAGE_LEDGER): return {}
    with open(BROKERAGE_LEDGER, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return json.loads(lines[-1]) if lines else {}

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    # 1. Fetch the raw data
    latest_record = get_latest_brokerage_record()
    brokerage_name = latest_record.get("brokerage_name", "Brokerage Partner Node")
    
    # 2. Run the analysis engine
    brief = generate_brokerage_analysis(BROKERAGE_LEDGER)
    
    # 3. Extract the confirmed data points
    status = brief.get('snapshot', {}).get('status', 'N/A')
    review = brief.get('review', {})
    what_happened = review.get('what_happened', 'No analysis available')
    what_means = review.get('what_it_means', 'No analysis available')
    
    # 4. Return the full HTML dashboard
    return f"""
    <html>
        <head>
            <style>
                body {{ font-family: sans-serif; padding: 40px; line-height: 1.6; background-color: #f4f7f6; }}
                .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Dashboard for {brokerage_name}</h1>
                <p><strong>Status:</strong> {status}</p>
                <hr>
                <h3>Executive Review</h3>
                <p><strong>What happened:</strong> {what_happened}</p>
                <p><strong>What it means:</strong> {what_means}</p>
            </div>
        </body>
    </html>
    """
