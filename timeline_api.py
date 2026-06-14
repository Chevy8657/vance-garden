from report_indexer import build_search_index

class TimelineAPI:
    def __init__(self):
        # Build the static artifact matrix on initialization
        self.index = build_search_index()

    def get_all_events(self):
        return list(self.index.values())

    def query_by_id(self, report_id):
        return self.index.get(report_id, None)

    def filter_timeline(self, risk_level=None, min_yield=None, assessment_type=None):
        """
        Executes granular queries against the read-only memory matrix.
        """
        results = list(self.index.values())
        
        if risk_level:
            results = [r for r in results if r.get('risk_level') == risk_level.upper()]
            
        if min_yield is not None:
            results = [r for r in results if r.get('efficiency_yield', 0) >= float(min_yield)]
            
        if assessment_type:
            results = [r for r in results if r.get('assessment_type') == assessment_type.upper()]
            
        # Sort chronologically by default
        results.sort(key=lambda x: x.get('generated_at', ''))
        return results

if __name__ == "__main__":
    api = TimelineAPI()
    print("[✓] Timeline API initialized.")
    print("Testing Filter (HIGH Risk):", api.filter_timeline(risk_level="HIGH"))
