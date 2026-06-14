# roadmap_engine.py

def generate_transformation_roadmap(current_readiness_score: float) -> dict:
    """
    Generates a high-conviction, value-driven 90-day onboarding sequencing map
    designed to expose hidden friction and elevate operations to world-class levels.
    """
    if current_readiness_score < 60.0:
        posture = "RESCUE_MODE"
        hidden_pain = "High structural margin leakage across split variations and severe administrative drag on top producers."
        primary_focus = "Immediate leak plugging and workflow stabilization."
    elif current_readiness_score < 80.0:
        posture = "OPTIMIZATION_READY"
        hidden_pain = "Fragmented recruiting pipelines and localized advisor production variance stalling division scaling."
        primary_focus = "Process automation and team scaling frameworks."
    else:
        posture = "CAPITAL_READY"
        hidden_pain = "Sub-optimized capital architecture and minor compliance reporting lag limiting institutional velocity."
        primary_focus = "Maximizing enterprise equity value and multi-market scaling."

    roadmap_sequence = {
        "posture": posture,
        "discovered_pain": hidden_pain,
        "strategic_focus": primary_focus,
        "action_plan": {
            "days_0_30": {
                "phase_title": "01 // INITIAL DOWNLOAD & ASSESSMENT",
                "objectives": [
                    "Execute complete ledger ingestion sequencing to map historical transaction variations.",
                    "Isolate and audit primary sources of hidden friction and margin leakage.",
                    "Establish baseline node connectivity and run full diagnostic compliance tracking."
                ]
            },
            "days_31_60": {
                "phase_title": "02 // FRICTION RESOLUTION & STABILIZATION",
                "objectives": [
                    "Deploy primary automated IPE modules to lock down validated leakage points.",
                    "Elevate transaction data workflows to world-class security and compliance baselines.",
                    "Automate high-drag administrative tasks to return operational capacity to leadership."
                ]
            },
            "days_61_90": {
                "phase_title": "03 // LIFESTYLE YIELD & VELOCITY",
                "objectives": [
                    "Verify net client gain metrics to confirm absolute zero operational cost increases.",
                    "Scale team onboarding sequences utilizing the standardized recruiting pipeline.",
                    "Lock in optimized baseline to achieve permanent high-performance node status."
                ]
            }
        },
        "foundry_guarantee": "We conduct the assessment, uncover the hidden pain, and seek to resolve it to world-class levels. More deals, less stress, bigger teams, no new costs. Try it if you like it—buy me lunch if you don't like it, just delete it."
    }
    
    return roadmap_sequence
