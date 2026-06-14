import json, os
class CarrierPropertyLink:
    def __init__(self, path="foundry_insurance/carrier_property_links.json"):
        self.path = path
        if not os.path.exists(self.path):
            with open(self.path, "w") as f: json.dump({}, f)
    def create_link(self, link_id, carrier_id, property_id, link_type):
        link = {"link_id": link_id, "carrier_id": carrier_id, "property_id": property_id, "status": "ACTIVE"}
        with open(self.path, "r+") as f:
            data = json.load(f); data[link_id] = link
            f.seek(0); json.dump(data, f, indent=4)
        return link
    def is_authorized(self, carrier_id, property_id):
        with open(self.path, "r") as f:
            data = json.load(f)
            return any(l["carrier_id"] == carrier_id and l["property_id"] == property_id for l in data.values())
