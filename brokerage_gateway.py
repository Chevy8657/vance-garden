import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime

from brokerage_brief import generate_brokerage_analysis
from impact_engine import calculate_foundry_impact
from roadmap_engine import generate_transformation_roadmap

app = FastAPI()
BROKERAGE_LEDGER = "/home/rick/pet_alpha/brokerage_ledger.json"

def get_latest_brokerage_record():
    if not os.path.exists(BROKERAGE_LEDGER): 
        return {}
    with open(BROKERAGE_LEDGER, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return json.loads(lines[-1]) if lines else {}

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    latest_record = get_latest_brokerage_record()
    brokerage_name = latest_record.get("brokerage_name", "Tracy Commercial Realty")
    
    raw_volume = latest_record.get("annual_volume", "325,000,000.00")
    if isinstance(raw_volume, str):
        raw_volume = raw_volume.replace("$", "").replace(",", "")
    volume = float(raw_volume)
    
    advisors = int(latest_record.get("advisors", 47))
    
    raw_readiness = latest_record.get("ownership_readiness", "72.5")
    if isinstance(raw_readiness, str):
        raw_readiness = raw_readiness.replace("%", "")
    readiness_score = float(raw_readiness)
    
    active_ipes_count = 4 
    brief = generate_brokerage_analysis(BROKERAGE_LEDGER)
    impact = calculate_foundry_impact(volume, advisors, active_ipes_count)
    roadmap = generate_transformation_roadmap(readiness_score)
    
    status = brief.get('snapshot', {}).get('status', 'ENTERPRISE SCALE')
    summary_text = brief.get('review', {}).get('summary', 'No summary available')
    what_happened = brief.get('review', {}).get('what_happened', '')
    what_it_means = brief.get('review', {}).get('what_it_means', '')
    rec_title = brief.get('review', {}).get('recommendation_title', 'Protect Margin Leakage')
    solution_mech = brief.get('review', {}).get('solution_mechanism', 'Optimization Engine')
    what_to_do = brief.get('review', {}).get('what_to_do_next', '')
    
    greatest_strength = brief.get('strengths', {}).get('greatest_strength', 'N/A')
    greatest_opportunity = brief.get('strengths', {}).get('greatest_opportunity', 'N/A')
    
    perf = brief.get("performance_breakdown", {"integrity": 50, "adoption": 50, "growth": 50, "contribution": 50})
    
    formatted_annual_value = "{:,}".format(impact["annual_value_created"])
    formatted_hours_returned = "{:,}".format(impact["hours_returned_annually"])
    formatted_net_gain = "{:,}".format(impact["net_value_created"])
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Foundry // Executive Brief</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&viewport=width-device-width');
            body {{ font-family: 'Inter', sans-serif; background-color: #0B0C10; color: #C5C6C7; }}
            .serif-title {{ font-family: 'Cinzel', serif; }}
            .mono-text {{ font-family: 'JetBrains Mono', monospace; }}
        </style>
    </head>
    <body class="p-8 max-w-7xl mx-auto">

        <!-- HEADER SECTION -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-zinc-800 pb-6 mb-8">
            <div>
                <h1 class="text-3xl font-bold tracking-tight text-white serif-title uppercase">{brokerage_name}</h1>
                <p class="text-xs tracking-widest text-zinc-500 uppercase mono-text mt-1">
                    Quarter 2 2026 Executive Brief // Vance Operating System
                </p>
            </div>
            <div class="mt-4 md:mt-0 bg-zinc-900 border border-zinc-800 px-4 py-2 rounded text-right">
                <span class="text-xs text-zinc-500 block uppercase tracking-wider mono-text">Node Status</span>
                <span class="text-sm font-semibold tracking-wide text-teal-400 font-mono">{status}</span>
            </div>
        </header>

        <!-- FOUNDRY ECONOMIC IMPACT HERO CARD -->
        <section class="bg-zinc-950 border border-zinc-800 rounded-xl p-6 mb-8 shadow-2xl">
            <h2 class="text-xs tracking-widest text-teal-500 font-bold uppercase mono-text mb-6">
                // FOUNDRY ECONOMIC OPERATING SYSTEM LIFTMETRICS //
            </h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <div class="border-b sm:border-b-0 sm:border-r border-zinc-800 pb-4 sm:pb-0 sm:pr-4">
                    <p class="text-xs tracking-wider text-zinc-500 uppercase mono-text">Annual Value Unlocked</p>
                    <p class="text-3xl font-bold tracking-tight text-emerald-400 mt-2">${formatted_annual_value}</p>
                </div>
                <div class="border-b lg:border-b-0 lg:border-r border-zinc-800 pb-4 sm:pb-0 sm:pr-4 lg:pl-4">
                    <p class="text-xs tracking-wider text-zinc-500 uppercase mono-text">Time Returned Annually</p>
                    <p class="text-3xl font-bold tracking-tight text-white mt-2">{formatted_hours_returned} hrs</p>
                </div>
                <div class="border-b sm:border-b-0 sm:border-r border-zinc-800 pb-4 sm:pb-0 sm:pr-4 lg:pl-4">
                    <p class="text-xs tracking-wider text-zinc-500 uppercase mono-text">FTE Reallocation Equivalent</p>
                    <p class="text-3xl font-bold tracking-tight text-white mt-2">{impact['fte_equivalent']} Staff</p>
                </div>
                <div class="lg:pl-4">
                    <p class="text-xs tracking-wider text-zinc-500 uppercase mono-text">Net Client Yield</p>
                    <p class="text-3xl font-bold tracking-tight text-indigo-400 mt-2">${formatted_net_gain}</p>
                </div>
            </div>
        </section>

        <!-- MAIN EXECUTIVE CONTENT CORES -->
        <main class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- LEFT & CENTER COLUMN -->
            <div class="lg:col-span-2 space-y-8">
                <div class="bg-zinc-900/40 border border-zinc-900 p-6 rounded-xl">
                    <h3 class="text-sm font-bold tracking-wider text-white uppercase mono-text border-b border-zinc-800 pb-3 mb-4">
                        01 // Strategic Operational Review
                    </h3>
                    <div class="space-y-4">
                        <div>
                            <span class="text-xs font-bold text-zinc-500 uppercase mono-text block">Discovered Reality:</span>
                            <p class="text-zinc-300 text-sm leading-relaxed mt-1">{what_happened if what_happened else summary_text}</p>
                        </div>
                        <div class="pt-2">
                            <span class="text-xs font-bold text-zinc-500 uppercase mono-text block">Structural Impact Vector:</span>
                            <p class="text-zinc-400 text-sm leading-relaxed mt-1">{what_it_means}</p>
                        </div>
                    </div>
                </div>

                <!-- CORE RATINGS METER MATRIX -->
                <div class="bg-zinc-900/40 border border-zinc-900 p-6 rounded-xl">
                    <h3 class="text-sm font-bold tracking-wider text-white uppercase mono-text border-b border-zinc-800 pb-3 mb-4">
                        02 // Core Capabilities Metric Matrix
                    </h3>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
                        <div class="bg-zinc-950 p-4 border border-zinc-800 rounded text-center">
                            <span class="text-[10px] uppercase text-zinc-500 tracking-wider font-mono">Integrity</span>
                            <div class="text-2xl font-bold text-teal-400 mt-1">{perf['integrity']}%</div>
                        </div>
                        <div class="bg-zinc-950 p-4 border border-zinc-800 rounded text-center">
                            <span class="text-[10px] uppercase text-zinc-500 tracking-wider font-mono">Adoption</span>
                            <div class="text-2xl font-bold text-teal-400 mt-1">{perf['adoption']}%</div>
                        </div>
                        <div class="bg-zinc-950 p-4 border border-zinc-800 rounded text-center">
                            <span class="text-[10px] uppercase text-zinc-500 tracking-wider font-mono">Growth</span>
                            <div class="text-2xl font-bold text-indigo-400 mt-1">{perf['growth']}%</div>
                        </div>
                        <div class="bg-zinc-950 p-4 border border-zinc-800 rounded text-center">
                            <span class="text-[10px] uppercase text-zinc-500 tracking-wider font-mono">Contribution</span>
                            <div class="text-2xl font-bold text-indigo-400 mt-1">{perf['contribution']}%</div>
                        </div>
                    </div>
                </div>

                <!-- 90 DAY ROADMAP SEQUENCE -->
                <div class="bg-zinc-900/40 border border-zinc-900 p-6 rounded-xl">
                    <h3 class="text-sm font-bold tracking-wider text-white uppercase mono-text border-b border-zinc-800 pb-3 mb-6">
                        03 // 90-Day Implementation Sequencing Map
                    </h3>
                    
                    <div class="space-y-6 relative border-l border-zinc-800 pl-6 ml-2">
                        <div class="relative">
                            <span class="absolute -left-[31px] top-0 bg-teal-500 w-3 h-3 rounded-full ring-4 ring-zinc-950"></span>
                            <h4 class="text-xs font-bold text-teal-400 uppercase mono-text">{roadmap['action_plan']['days_0_30']['phase_title']}</h4>
                            <ul class="mt-2 space-y-1.5 text-xs text-zinc-400 list-disc list-inside">
                                <li>{roadmap['action_plan']['days_0_30']['objectives'][0]}</li>
                                <li>{roadmap['action_plan']['days_0_30']['objectives'][1]}</li>
                                <li>{roadmap['action_plan']['days_0_30']['objectives'][2]}</li>
                            </ul>
                        </div>
                        <div class="relative">
                            <span class="absolute -left-[31px] top-0 bg-indigo-500 w-3 h-3 rounded-full ring-4 ring-zinc-950"></span>
                            <h4 class="text-xs font-bold text-indigo-400 uppercase mono-text">{roadmap['action_plan']['days_31_60']['phase_title']}</h4>
                            <ul class="mt-2 space-y-1.5 text-xs text-zinc-400 list-disc list-inside">
                                <li>{roadmap['action_plan']['days_31_60']['objectives'][0]}</li>
                                <li>{roadmap['action_plan']['days_31_60']['objectives'][1]}</li>
                                <li>{roadmap['action_plan']['days_31_60']['objectives'][2]}</li>
                            </ul>
                        </div>
                        <div class="relative">
                            <span class="absolute -left-[31px] top-0 bg-zinc-700 w-3 h-3 rounded-full ring-4 ring-zinc-950"></span>
                            <h4 class="text-xs font-bold text-zinc-500 uppercase mono-text">{roadmap['action_plan']['days_61_90']['phase_title']}</h4>
                            <ul class="mt-2 space-y-1.5 text-xs text-zinc-400 list-disc list-inside">
                                <li>{roadmap['action_plan']['days_61_90']['objectives'][0]}</li>
                                <li>{roadmap['action_plan']['days_61_90']['objectives'][1]}</li>
                                <li>{roadmap['action_plan']['days_61_90']['objectives'][2]}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- RIGHT COLUMN: ADVISORY MANDATE -->
            <div class="space-y-8">
                <div class="bg-gradient-to-b from-zinc-900 to-zinc-950 border border-zinc-800 p-6 rounded-xl shadow-lg">
                    <span class="text-[10px] tracking-widest text-zinc-500 uppercase mono-text font-bold block mb-1">Vance Advisory Mandate</span>
                    <h3 class="text-lg font-bold text-white tracking-tight leading-snug">{rec_title}</h3>
                    
                    <div class="mt-4 pt-4 border-t border-zinc-800/60">
                        <span class="text-xs font-bold text-teal-400 uppercase font-mono block">Resolution Architecture:</span>
                        <p class="text-xs text-zinc-300 mt-1 font-semibold">{solution_mech}</p>
                    </div>

                    <div class="mt-4">
                        <span class="text-xs font-bold text-zinc-500 uppercase mono-text block">Immediate Directive:</span>
                        <p class="text-xs text-zinc-400 leading-relaxed mt-1">{what_to_do}</p>
                    </div>
                </div>

                <div class="bg-zinc-900/20 border border-zinc-900 p-5 rounded-xl text-xs space-y-4">
                    <div>
                        <span class="text-zinc-500 uppercase font-bold tracking-wider block mono-text">Primary Asset Anchor</span>
                        <p class="text-zinc-300 font-semibold mt-0.5">{greatest_strength}</p>
                    </div>
                    <div>
                        <span class="text-zinc-500 uppercase font-bold tracking-wider block mono-text">Primary Target Arbitrage</span>
                        <p class="text-zinc-300 font-semibold mt-0.5">{greatest_opportunity}</p>
                    </div>
                    <div>
                        <span class="text-zinc-500 uppercase font-bold tracking-wider block mono-text">Active Structural IPE Count</span>
                        <p class="text-zinc-300 font-mono mt-0.5">{active_ipes_count} Deployed Elements</p>
                    </div>
                </div>
            </div>
        </main>

        <!-- FOOTER GUARANTEE -->
        <footer class="mt-12 p-6 bg-zinc-950 border border-zinc-900 rounded-xl text-center">
            <h3 class="text-[10px] font-bold tracking-widest text-zinc-600 uppercase mono-text mb-2">// THE FOUNDRY SYSTEM AGREEMENT //</h3>
            <p class="text-xs text-zinc-400 max-w-3xl mx-auto italic leading-relaxed">
                "{roadmap['foundry_guarantee']}"
            </p>
        </footer>

    </body>
    </html>
    """
