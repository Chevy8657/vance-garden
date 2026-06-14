from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Any, Optional


@dataclass
class RealityCard:
    id: str
    scope: str
    category: str
    title: str
    metric_name: str
    current_value: float
    target_value: float
    severity: str
    discovered_reality: str
    affected_group: str
    source: str
    status: str = "open"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ActionPack:
    id: str
    reality_card_id: str
    ipe: str
    title: str
    priority: str
    summary: str
    prepared_actions: List[str]
    expected_impact: Dict[str, Any]
    review_time_minutes: int
    approval_options: List[str] = field(default_factory=lambda: ["approve", "modify", "snooze", "dismiss"])
    status: str = "prepared"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ApprovalDecision:
    id: str
    action_pack_id: str
    decision: str
    approved_by: str
    scope: Dict[str, Any]
    notes: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CapacityLedgerEntry:
    id: str
    action_pack_id: str
    capacity_goal_hours: float
    actual_capacity_returned_hours: float
    measurement_period: str
    evidence: List[str]
    status: str = "tracking"

    def goal_achievement_percent(self) -> float:
        if self.capacity_goal_hours <= 0:
            return 0.0
        return round((self.actual_capacity_returned_hours / self.capacity_goal_hours) * 100, 1)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["goal_achievement_percent"] = self.goal_achievement_percent()
        return data


class VanceRecommendationEngine:
    """
    IPE-10: VANCE Performance Concierge Engine

    Engine Flow:
    Assessment/Data
        -> RealityCard
        -> ActionPack
        -> Review & Approve
        -> CapacityLedgerEntry
    """

    def __init__(self):
        self.reality_cards: List[RealityCard] = []
        self.action_packs: List[ActionPack] = []
        self.capacity_ledger: List[CapacityLedgerEntry] = []
        self.approval_decisions: List[ApprovalDecision] = []
        self._load_sample_engine_state()

    def _load_sample_engine_state(self) -> None:
        self.reality_cards = [
            RealityCard(
                id="RC-001",
                scope="brokerage",
                category="Compliance",
                title="Transaction file completeness below target",
                metric_name="audit_ready_file_score",
                current_value=72,
                target_value=95,
                severity="high",
                discovered_reality="28% of reviewed transaction files are missing required documentation or signatures.",
                affected_group="Active transaction files",
                source="VANCE Discovery Assessment",
            ),
            RealityCard(
                id="RC-002",
                scope="brokerage",
                category="Opportunity Recovery",
                title="Lead response time exceeds target",
                metric_name="median_lead_response_minutes",
                current_value=46,
                target_value=5,
                severity="high",
                discovered_reality="Inbound leads are not being contacted within the brokerage response goal.",
                affected_group="Inbound buyer and seller leads",
                source="VANCE Discovery Assessment",
            ),
            RealityCard(
                id="RC-003",
                scope="office",
                category="Administrative Drag",
                title="Manual back-office workload restricting capacity",
                metric_name="manual_admin_hours_weekly",
                current_value=18,
                target_value=6,
                severity="medium",
                discovered_reality="Administrative staff are spending significant time chasing file status, missing documents, and duplicate updates.",
                affected_group="Transaction coordination and broker review staff",
                source="VANCE Discovery Assessment",
            ),
        ]

        self.action_packs = [
            ActionPack(
                id="AP-001",
                reality_card_id="RC-001",
                ipe="Compliance Readiness",
                title="Transaction File Clean-Up Sprint",
                priority="high",
                summary="VANCE recommends a focused compliance clean-up sprint to reduce audit exposure and missing documentation.",
                prepared_actions=[
                    "Identify active transaction files missing required documents",
                    "Notify responsible agents with a targeted document request",
                    "Set a 48-hour correction window",
                    "Escalate unresolved files to broker review",
                    "Update the audit-ready file score after correction",
                ],
                expected_impact={
                    "monthly_capacity_goal_per_user_hours": 8,
                    "risk_reduction": "Medium-High",
                    "primary_outcome": "Improved audit readiness",
                },
                review_time_minutes=2,
            ),
            ActionPack(
                id="AP-002",
                reality_card_id="RC-002",
                ipe="Opportunity Recovery",
                title="Lead Response Protocol",
                priority="high",
                summary="VANCE recommends a lead response protocol to reduce lead leakage and improve conversion discipline.",
                prepared_actions=[
                    "Define broker-approved lead response target",
                    "Flag leads with no recorded follow-up inside the target window",
                    "Notify assigned agent when response target is missed",
                    "Prepare reassignment recommendation for stale leads",
                    "Track recovered opportunities in the Capacity Ledger",
                ],
                expected_impact={
                    "monthly_capacity_goal_per_user_hours": 10,
                    "opportunity_protection": "High",
                    "primary_outcome": "Reduced lead leakage",
                },
                review_time_minutes=3,
            ),
            ActionPack(
                id="AP-003",
                reality_card_id="RC-003",
                ipe="Capacity Recovery",
                title="Administrative Drag Reduction Pack",
                priority="medium",
                summary="VANCE recommends reducing repetitive admin work through standard checklists, status visibility, and prepared follow-up actions.",
                prepared_actions=[
                    "Identify recurring manual status requests",
                    "Create a centralized file status view",
                    "Prepare standard follow-up templates",
                    "Reduce duplicate coordinator updates",
                    "Measure administrative capacity returned weekly",
                ],
                expected_impact={
                    "monthly_capacity_goal_per_user_hours": 12,
                    "efficiency_gain": "Medium",
                    "primary_outcome": "Reduced administrative drag",
                },
                review_time_minutes=4,
            ),
        ]

        self.capacity_ledger = [
            CapacityLedgerEntry(
                id="CL-001",
                action_pack_id="AP-001",
                capacity_goal_hours=8,
                actual_capacity_returned_hours=5.5,
                measurement_period="monthly",
                evidence=[
                    "Reduced manual file review time",
                    "Fewer missing signature follow-ups",
                    "Improved audit-ready file score",
                ],
            ),
            CapacityLedgerEntry(
                id="CL-002",
                action_pack_id="AP-002",
                capacity_goal_hours=10,
                actual_capacity_returned_hours=6,
                measurement_period="monthly",
                evidence=[
                    "Faster lead response tracking",
                    "Reduced number of untouched inbound leads",
                    "Recovered dormant opportunity candidates",
                ],
            ),
            CapacityLedgerEntry(
                id="CL-003",
                action_pack_id="AP-003",
                capacity_goal_hours=12,
                actual_capacity_returned_hours=7.5,
                measurement_period="monthly",
                evidence=[
                    "Reduced coordinator status emails",
                    "Centralized action visibility",
                    "Fewer duplicate manual updates",
                ],
            ),
        ]

    def get_reality_cards(self) -> List[Dict[str, Any]]:
        return [card.to_dict() for card in self.reality_cards]

    def get_action_packs(self) -> List[Dict[str, Any]]:
        return [pack.to_dict() for pack in self.action_packs]

    def get_capacity_ledger(self) -> List[Dict[str, Any]]:
        return [entry.to_dict() for entry in self.capacity_ledger]

    def get_action_pack(self, action_pack_id: str) -> Optional[Dict[str, Any]]:
        for pack in self.action_packs:
            if pack.id == action_pack_id:
                return pack.to_dict()
        return None

    def get_reality_card(self, reality_card_id: str) -> Optional[Dict[str, Any]]:
        for card in self.reality_cards:
            if card.id == reality_card_id:
                return card.to_dict()
        return None

    def get_action_with_reality(self, action_pack_id: str) -> Optional[Dict[str, Any]]:
        action = self.get_action_pack(action_pack_id)
        if not action:
            return None

        reality = self.get_reality_card(action["reality_card_id"])
        return {
            "reality_card": reality,
            "action_pack": action,
        }

    def record_decision(
        self,
        action_pack_id: str,
        decision: str,
        approved_by: str = "Broker Owner",
        scope: Optional[Dict[str, Any]] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        if scope is None:
            scope = {
                "offices": ["Primary Office"],
                "agents": "all",
                "duration_days": 14,
            }

        decision_id = f"AD-{len(self.approval_decisions) + 1:03d}"

        approval = ApprovalDecision(
            id=decision_id,
            action_pack_id=action_pack_id,
            decision=decision,
            approved_by=approved_by,
            scope=scope,
            notes=notes,
        )

        self.approval_decisions.append(approval)

        for pack in self.action_packs:
            if pack.id == action_pack_id:
                pack.status = decision

        return approval.to_dict()


    def get_morning_brief(self) -> Dict[str, Any]:
        """
        Daily VANCE habit loop.

        This summarizes what VANCE handled while the user was away and
        gives the broker a short review queue instead of a pile of work.
        """
        actions_prepared = len(self.action_packs)
        decisions_required = len([p for p in self.action_packs if p.status == "prepared"])
        high_priority = len([p for p in self.action_packs if p.priority == "high"])

        return {
            "title": "While You Were Away",
            "items_reviewed": 12,
            "communications_categorized": 43,
            "admin_requests_prepared": 17,
            "actions_prepared": actions_prepared,
            "opportunities_identified": 2,
            "decisions_required": decisions_required,
            "high_priority_items": high_priority,
            "estimated_review_time_minutes": 3,
            "message": (
                "VANCE reviewed operational activity, organized routine work, "
                "prepared recommended actions, and surfaced only the decisions "
                "requiring broker review."
            ),
        }


    def get_change_manager(self) -> Dict[str, Any]:
        """
        Change Manager:
        Tracks approved action plans, current change status, and historical improvement evidence.
        """
        completed_changes = [
            {
                "id": "CH-001",
                "title": "Transaction File Clean-Up Sprint",
                "status": "completed",
                "category": "Required By Law",
                "approved_date": "2026-06-01",
                "completed_date": "2026-06-12",
                "before_metric": "Audit-ready file score: 81%",
                "after_metric": "Audit-ready file score: 97%",
                "capacity_returned_hours": 18,
                "result": "File deficiencies reduced and compliance readiness improved."
            },
            {
                "id": "CH-002",
                "title": "Lead Response Protocol",
                "status": "in_progress",
                "category": "Value Added",
                "approved_date": "2026-06-08",
                "completed_date": "Pending",
                "before_metric": "Median lead response: 46 minutes",
                "after_metric": "Target response: under 5 minutes",
                "capacity_returned_hours": 6,
                "result": "Lead leakage reduction currently being monitored."
            },
            {
                "id": "CH-003",
                "title": "Administrative Drag Reduction Pack",
                "status": "awaiting_measurement",
                "category": "Non-Value Added",
                "approved_date": "2026-06-10",
                "completed_date": "Pending",
                "before_metric": "Manual admin workload: 18 hrs/week",
                "after_metric": "Target workload: 6 hrs/week",
                "capacity_returned_hours": 7.5,
                "result": "Coordinator workload reduction pending validation."
            }
        ]

        return {
            "title": "Change Manager",
            "subtitle": "Every approved action becomes part of the improvement record.",
            "pending_review": len([p for p in self.action_packs if p.status == "prepared"]),
            "implemented": len([p for p in self.action_packs if p.status == "implemented"]),
            "in_progress": len([c for c in completed_changes if c["status"] == "in_progress"]),
            "awaiting_measurement": len([c for c in completed_changes if c["status"] == "awaiting_measurement"]),
            "completed": len([c for c in completed_changes if c["status"] == "completed"]),
            "total_capacity_returned_hours": sum(c["capacity_returned_hours"] for c in completed_changes),
            "changes": completed_changes,
        }

    def get_work_classification(self) -> Dict[str, Any]:
        """
        Work Classification:
        Categorizes activity into Value Added, Required By Law, and Non-Value Added work.
        """
        return {
            "title": "Work Classification",
            "summary": "VANCE helps reduce red work, simplify yellow work, and expand green work.",
            "categories": [
                {
                    "name": "Value Added",
                    "label": "Green Work",
                    "percent": 25,
                    "goal": 45,
                    "description": "Client conversations, listing appointments, recruiting, growth, and relationship building.",
                    "direction": "Increase"
                },
                {
                    "name": "Required By Law",
                    "label": "Yellow Work",
                    "percent": 30,
                    "goal": 25,
                    "description": "Compliance reviews, disclosures, audits, retention, licensing, and required documentation.",
                    "direction": "Simplify"
                },
                {
                    "name": "Non-Value Added",
                    "label": "Red Work",
                    "percent": 45,
                    "goal": 30,
                    "description": "Status chasing, rework, duplicate entry, wondering, wandering, watching, overprocessing, COPQ, assumptions, and poor coordination.",
                    "direction": "Eliminate"
                }
            ],
            "top_waste_sources": [
                "Status chasing",
                "Document hunting",
                "Duplicate data entry",
                "Rework",
                "Lack of communication",
                "Lack of coordination",
                "Assumption-based work",
                "Decision latency",
                "Overprocessing",
                "Leadership friction"
            ]
        }

    def get_while_away(self) -> Dict[str, Any]:
        """
        While You Were Away:
        Shows what VANCE handled while the user was sleeping, away, off-clock, or focused elsewhere.
        """
        return {
            "title": "While You Were Away",
            "protected_period": "Since your last login",
            "items_reviewed": 12,
            "communications_categorized": 43,
            "admin_requests_prepared": 17,
            "actions_prepared": len(self.action_packs),
            "critical_items": 1,
            "decisions_required": len([p for p in self.action_packs if p.status == "prepared"]),
            "estimated_catchup_time_minutes": 7,
            "calendar_intrusions_prevented": 9,
            "message": "VANCE organized routine work, prepared actions, deferred non-critical interruptions, and surfaced only the items requiring review."
        }

    def get_dashboard_summary(self) -> Dict[str, Any]:
        open_reality_cards = [card for card in self.reality_cards if card.status == "open"]
        high_priority_actions = [pack for pack in self.action_packs if pack.priority == "high"]

        total_capacity_goal = sum(entry.capacity_goal_hours for entry in self.capacity_ledger)
        total_capacity_returned = sum(entry.actual_capacity_returned_hours for entry in self.capacity_ledger)

        if total_capacity_goal > 0:
            goal_progress = round((total_capacity_returned / total_capacity_goal) * 100, 1)
        else:
            goal_progress = 0.0

        return {
            "greeting": "Good Afternoon, Tracy",
            "commission_neutral_statement": (
                "VANCE helps recover time, reduce friction, identify critical path issues, "
                "and prepare actions for review while never participating in real estate commissions."
            ),
            "reality_cards_open": len(open_reality_cards),
            "actions_prepared": len(self.action_packs),
            "high_priority_actions": len(high_priority_actions),
            "monthly_capacity_goal_per_user_hours": 40,
            "capacity_returned_hours": round(total_capacity_returned, 1),
            "capacity_goal_progress_percent": goal_progress,
            "opportunities_recovered": 2,
            "compliance_score": 97,
            "compliance_delta": 5,
        }


if __name__ == "__main__":
    engine = VanceRecommendationEngine()

    print("VANCE ENGINE ONLINE")
    print("===================")
    print(engine.get_dashboard_summary())

    print("\nREALITY CARDS")
    print("-------------")
    for card in engine.get_reality_cards():
        print(card)

    print("\nACTION PACKS")
    print("------------")
    for action in engine.get_action_packs():
        print(action)

    print("\nCAPACITY LEDGER")
    print("---------------")
    for entry in engine.get_capacity_ledger():
        print(entry)
