class TransformationTimelineEngine:

    @staticmethod
    def build(current_ipe, target_ipe):

        gap = target_ipe - current_ipe

        quarter_1 = min(current_ipe + round(gap * 0.30), target_ipe)
        quarter_2 = min(current_ipe + round(gap * 0.60), target_ipe)
        quarter_3 = min(current_ipe + round(gap * 0.85), target_ipe)
        quarter_4 = target_ipe

        return {
            "current_ipe": current_ipe,
            "target_ipe": target_ipe,
            "day_0": current_ipe,
            "day_90": quarter_1,
            "day_180": quarter_2,
            "day_270": quarter_3,
            "day_360": quarter_4,
            "destination": "Compliant Node Owner"
        }
