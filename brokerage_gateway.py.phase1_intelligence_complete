import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from datetime import datetime
from brokerage_brief import generate_brokerage_analysis
from brokerage_data import load_brokerage_records

app = FastAPI()
templates = Jinja2Templates(directory="templates")
BROKERAGE_LEDGER = "/home/rick/pet_alpha/brokerage_ledger.json"

def get_latest_brokerage_record():
    if not os.path.exists(BROKERAGE_LEDGER): return {}
    with open(BROKERAGE_LEDGER, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return json.loads(lines[-1]) if lines else {}

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    latest_record = get_latest_brokerage_record()
    brokerage_name = latest_record.get("brokerage_name", "Brokerage Partner Node")
    brief = generate_brokerage_analysis(BROKERAGE_LEDGER)

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "brokerage_name": brokerage_name,
            "snapshot": brief.get("snapshot", {}),
            "review": brief.get("review", {}),
            "strengths": brief.get("strengths", {}),
            "action_plan": brief.get("action_plan", {}),
            "debug": brief.get("debug", {}),
        }
    )


@app.get("/clients", response_class=HTMLResponse)
async def clients_page(request: Request):
    records = load_brokerage_records()

    latest_by_client = {}
    for r in records:
        name = r.get("brokerage_name", "Unknown Brokerage")
        latest_by_client[name] = r

    records = list(latest_by_client.values())
    records.sort(key=lambda x: x.get("brokerage_name", ""))

    return templates.TemplateResponse(
        request=request,
        name="clients.html",
        context={"records": records}
    )


@app.get("/client/{client_name}", response_class=HTMLResponse)
async def client_detail_page(request: Request, client_name: str):
    records = load_brokerage_records()

    matches = [
        r for r in records
        if r.get("brokerage_name", "").lower() == client_name.lower()
    ]

    if not matches:
        return HTMLResponse("<h1>Client not found</h1>", status_code=404)

    latest = matches[-1]

    return templates.TemplateResponse(
        request=request,
        name="client_detail.html",
        context={
            "client": latest,
            "history": matches[::-1],
            "assessment_count": len(matches)
        }
    )
