class ExecutiveScorecardEngine:

    @staticmethod
    def build(
        self_assessment,
        vance_assessment,
        target_score
    ):

        perception_gap = (
            self_assessment -
            vance_assessment
        )

        goal_gap = (
            target_score -
            vance_assessment
        )

        if goal_gap >= 40:
            transformation_priority = "Critical Transformation"

        elif goal_gap >= 25:
            transformation_priority = "Strategic Improvement"

        elif goal_gap >= 10:
            transformation_priority = "Optimization"

        else:
            transformation_priority = "Sustain & Monitor"

        return {
            "self_assessment": self_assessment,
            "vance_assessment": vance_assessment,
            "target_score": target_score,
            "perception_gap": perception_gap,
            "goal_gap": goal_gap,
            "transformation_priority": transformation_priority
        }
