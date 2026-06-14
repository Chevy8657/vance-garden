import os
import json
import glob
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="V.A.N.C.E. Engine Gateway", version="1.3.0")

LEDGER_PATH = "ledger.json"
ARCHIVE_DIR = "archive"

NODE_SECURITY_TOKEN = os.getenv("VANCE_NODE_TOKEN", "SovereignNodeSecret2026")

async def verify_node_signature(x_node_token: str = Header(None)):
    if x_node_token is None:
        raise HTTPException(status_code=401, detail="Authentication signature missing from request header.")
    if x_node_token != NODE_SECURITY_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid node token signature. Access denied.")
    return x_node_token

class OfficeSubmission(BaseModel):
    office_name: str = Field(..., example="Foundry District Alpha")
    office_status: str = Field(default="GROWTH PHASE", example="GROWTH PHASE")
    readiness_score: int = Field(..., ge=0, le=100, example=92)
    annual_impact: float = Field(..., ge=0.0, example=214000.0)
    recommendation: str = Field(..., example="Growth Module + Marketing Concierge")
    notes: Optional[str] = Field(default=None, example="Initial testing data entry.")

@app.get("/")
async def root():
    return {
        "status": "ONLINE",
        "engine": "V.A.N.C.E.",
        "timestamp": datetime.utcnow().isoformat(),
        "security_mode": "ENFORCED"
    }

@app.post("/submit", status_code=201, dependencies=[Depends(verify_node_signature)])
async def submit_to_ledger(payload: OfficeSubmission):
    try:
        record = payload.model_dump()
        record["timestamp"] = datetime.utcnow().isoformat()
        
        with open(LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
            
        return {
            "status": "SUCCESS",
            "message": "Data recorded to sovereign ledger via verified stream.",
            "tracked_office": record["office_name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sovereign write failure: {str(e)}")

@app.post("/brief/generate")
async def generate_brief_endpoint():
    if not os.path.exists(LEDGER_PATH) or os.path.getsize(LEDGER_PATH) == 0:
        return {"status": "EMPTY", "analysis": "No data found in the current sovereign ledger cycle."}
    
    try:
        from brief import generate_executive_analysis
        analysis_result = generate_executive_analysis(LEDGER_PATH)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis engine error: {str(e)}")

@app.get("/ledger/verify")
async def verify_ledger_integrity():
    if not os.path.exists(LEDGER_PATH) or os.path.getsize(LEDGER_PATH) == 0:
        return {"status": "CLEAN", "line_count": 0, "corrupt_lines_detected": 0, "message": "Runway is completely clear."}
        
    corrupt_count = 0
    total_lines = 0
    with open(LEDGER_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total_lines += 1
            try:
                json.loads(line)
            except json.JSONDecodeError:
                corrupt_count += 1
                
    return {
        "status": "AUDITED" if corrupt_count == 0 else "WARNING_CORRUPTION_DETECTED",
        "line_count": total_lines,
        "corrupt_lines_detected": corrupt_count,
        "integrity_certified": corrupt_count == 0
    }

def get_manifests_internal():
    search_path = os.path.join(ARCHIVE_DIR, "manifest_*.json")
    manifest_files = glob.glob(search_path)
    historical_timeline = []
    
    for file_path in sorted(manifest_files, reverse=True):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                manifest_data = json.load(f)
                historical_timeline.append({
                    "file_name": os.path.basename(file_path),
                    "snapshot_metrics": manifest_data.get("summary", {}),
                    "governance_verdict": manifest_data.get("predictive_risk_model", {}).get("network_risk_velocity", "UNKNOWN")
                })
        except Exception:
            continue
    return historical_timeline

@app.get("/ledger/manifests")
async def list_archived_manifests():
    timeline = get_manifests_internal()
    return {
        "archive_directory": ARCHIVE_DIR,
        "total_archived_cycles": len(timeline),
        "timeline": timeline
    }

@app.post("/ledger/archive", dependencies=[Depends(verify_node_signature)])
async def archive_ledger_cycle():
    if not os.path.exists(LEDGER_PATH) or os.path.getsize(LEDGER_PATH) == 0:
        raise HTTPException(status_code=400, detail="Active ledger is empty. Cycle rotation aborted.")
        
    try:
        from brief import generate_executive_analysis
        final_analysis = generate_executive_analysis(LEDGER_PATH)
        
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        timestamp_token = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        manifest_filename = f"{ARCHIVE_DIR}/manifest_{timestamp_token}.json"
        ledger_backup_filename = f"{ARCHIVE_DIR}/ledger_{timestamp_token}.json"
        
        with open(manifest_filename, "w", encoding="utf-8") as f:
            json.dump(final_analysis, f, indent=4)
            
        os.rename(LEDGER_PATH, ledger_backup_filename)
        open(LEDGER_PATH, "w").close()
        
        return {
            "status": "ROTATED",
            "message": "State safely cleared and committed to archival history.",
            "certified_manifest": manifest_filename,
            "historical_ledger_log": ledger_backup_filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State rotation failure: {str(e)}")

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_admin_dashboard():
    # 1. Gather Active Data Context
    active_count = 0
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r", encoding="utf-8") as f:
            active_count = sum(1 for line in f if line.strip())
            
    from brief import generate_executive_analysis
    if active_count > 0:
        active_analysis = generate_executive_analysis(LEDGER_PATH)
        summary = active_analysis.get("summary", {})
        risk_model = active_analysis.get("predictive_risk_model", {})
        active_impact = summary.get("cumulative_annual_impact", "$0.00")
        active_readiness = f"{summary.get('average_network_readiness', 0)}%"
        risk_velocity = risk_model.get("network_risk_velocity", "STABLE")
        gov_action = risk_model.get("adaptive_governance_action", "All clear.")
    else:
        active_impact = "$0.00"
        active_readiness = "N/A"
        risk_velocity = "EMPTY"
        gov_action = "Runway clear. Awaiting secure incoming stream node inputs."

    # 2. Gather Historical Archives
    timeline = get_manifests_internal()
    timeline_html = ""
    
    if not timeline:
        timeline_html = '<div class="text-gray-500 italic p-4 bg-zinc-900 border border-zinc-800 rounded">No historical manifests committed yet.</div>'
    else:
        for item in timeline:
            metrics = item["snapshot_metrics"]
            verdict = item["governance_verdict"]
            
            # Contextual alert pills
            badge_color = "text-emerald-400 bg-emerald-950/40 border-emerald-800"
            if "ATTENTION" in verdict:
                badge_color = "text-amber-400 bg-amber-950/40 border-amber-800"
            elif "CRITICAL" in verdict:
                badge_color = "text-rose-400 bg-rose-950/40 border-rose-800"
                
            timeline_html += f"""
            <div class="bg-zinc-900/60 p-5 rounded border border-zinc-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 transition-all hover:border-zinc-700">
                <div>
                    <div class="text-sm font-mono text-zinc-500 mb-1">{item['file_name']}</div>
                    <div class="grid grid-cols-2 sm:grid-cols-3 gap-x-8 gap-y-1 text-sm">
                        <div><span class="text-zinc-400 text-xs">Evaluated Nodes:</span> <span class="text-zinc-200 font-medium font-mono">{metrics.get('total_offices_evaluated', 0)}</span></div>
                        <div><span class="text-zinc-400 text-xs">Total Impact:</span> <span class="text-[#20B2AA] font-medium font-mono">{metrics.get('cumulative_annual_impact', '$0.00')}</span></div>
                        <div><span class="text-zinc-400 text-xs">Avg Readiness:</span> <span class="text-zinc-200 font-medium font-mono">{metrics.get('average_network_readiness', 0)}%</span></div>
                    </div>
                </div>
                <div class="px-3 py-1 rounded text-xs font-mono font-semibold tracking-wider border {badge_color}">
                    {verdict}
                </div>
            </div>
            """

    # Velocity status color mappings
    status_class = "text-emerald-400 bg-emerald-950/20 border-emerald-900"
    if "ATTENTION" in risk_velocity:
        status_class = "text-amber-400 bg-amber-950/20 border-amber-900"
    elif "CRITICAL" in risk_velocity:
        status_class = "text-rose-400 bg-rose-950/20 border-rose-900"
    elif "EMPTY" in risk_velocity:
        status_class = "text-zinc-500 bg-zinc-950/20 border-zinc-800"

    # Embedded CSS & Structure definition
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>V.A.N.C.E. Network Governance Control</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #0B0C10; }}
        </style>
    </head>
    <body class="text-zinc-100 min-h-screen flex flex-col antialiased font-sans px-4 sm:px-8 py-8 selection:bg-[#20B2AA] selection:text-black">
        <header class="max-w-6xl w-full mx-auto border-b border-zinc-800 pb-6 mb-8 flex justify-between items-center">
            <div>
                <h1 class="text-xl font-bold tracking-wider text-zinc-100 font-mono">V.A.N.C.E. <span class="text-[#20B2AA]">ENGINE</span></h1>
                <p class="text-xs text-zinc-500 tracking-tight font-mono mt-0.5">Sovereign Decentralized Infrastructure Management</p>
            </div>
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span class="text-xs font-mono font-bold tracking-widest text-zinc-400">GATEWAY ONLINE</span>
            </div>
        </header>

        <main class="max-w-6xl w-full mx-auto flex-1 grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-1 flex flex-col gap-6">
                <h2 class="text-xs font-mono tracking-widest uppercase text-zinc-400 font-bold border-l-2 border-[#20B2AA] pl-2">Active Runway State</h2>
                
                <div class="bg-zinc-900/40 border border-zinc-800 rounded p-6 flex flex-col gap-5">
                    <div>
                        <div class="text-xs text-zinc-500 font-mono uppercase tracking-wide">Staged Network Changes</div>
                        <div class="text-4xl font-mono font-bold mt-1 text-zinc-100">{active_count} <span class="text-xs text-zinc-500">nodes</span></div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 border-t border-b border-zinc-800/80 py-4 font-mono">
                        <div>
                            <div class="text-[10px] text-zinc-500 uppercase tracking-wide">Cumulative Impact</div>
                            <div class="text-sm font-semibold text-[#20B2AA] mt-0.5">{active_impact}</div>
                        </div>
                        <div>
                            <div class="text-[10px] text-zinc-500 uppercase tracking-wide font-mono">Avg Readiness</div>
                            <div class="text-sm font-semibold text-zinc-200 mt-0.5">{active_readiness}</div>
                        </div>
                    </div>
                    <div>
                        <div class="text-xs text-zinc-500 font-mono uppercase tracking-wide mb-2">Risk Velocity Metric</div>
                        <div class="border rounded p-3 font-mono text-xs font-medium leading-relaxed {status_class}">
                            <div class="font-bold tracking-wider mb-1 uppercase text-[10px] opacity-90">Verdict: {risk_velocity}</div>
                            {gov_action}
                        </div>
                    </div>
                </div>
            </div>

            <div class="lg:col-span-2 flex flex-col gap-6">
                <h2 class="text-xs font-mono tracking-widest uppercase text-zinc-400 font-bold border-l-2 border-[#DAA520] pl-2">Archived Manifest Explorer</h2>
                <div class="flex flex-col gap-3">
                    {timeline_html}
                </div>
            </div>
        </main>
        
        <footer class="max-w-6xl w-full mx-auto border-t border-zinc-900 mt-12 pt-4 text-center text-[10px] font-mono text-zinc-600 tracking-widest">
            VANCE ENGINE v1.3.0 // EXECUTING ATOMIC DATA OPERATIONS LOCAL-FIRST
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
