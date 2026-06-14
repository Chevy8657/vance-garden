import json
import sys

sys.path.append('/home/rick/pet_alpha/target_adapter')
sys.path.append('/home/rick/pet_alpha')

from intake_normalizer import TargetIntakeNormalizer
from broker_event_mapper import BrokerEventMapper
from evidence_packet_builder import EvidencePacketBuilder
from network_gateway import inspect_ingress_clearance
from core_ingestion_sink import verify_and_ingest_packet

def run_integration_pipeline():
    print("="*90)
    print("RUNNING ADAPTER TO CORE INGESTION SINK SPRINT 10 RUN")
    print("="*90)

    normalizer = TargetIntakeNormalizer()
    mapper = BrokerEventMapper()
    builder = EvidencePacketBuilder(node_signing_key="FOUNDRY_SECRET_SECURE_TOKEN_2026")

    # 1. Parse Data
    with open('/home/rick/pet_alpha/target_adapter/sample_payloads/raw_broker_lead.json', 'r') as f:
        raw_payload = json.load(f)

    sterile_obj = normalizer.normalize_external_payload(raw_payload)
    mapped_obj = mapper.map_to_internal_spec(sterile_obj)
    
    # Generate unique test packet footprint
    simulated_id = f"PKT-TX-{int(sys.argv[1]) if len(sys.argv) > 1 else 101}"
    sealed_packet = builder.seal_evidence_packet(mapped_obj, simulated_packet_id=simulated_id)

    # 2. Gate Perimeter Verification
    decision, msg = inspect_ingress_clearance(sealed_packet["origin_node"])
    print(f"[🛡️ GATEWAY] Clearance check: {decision} -> {msg}")
    
    if decision != "APPROVED":
        print("\033[38;5;196m[✕] Dropped at perimeter.\033[0m")
        return

    # 3. Push to Core Ingestion Sink
    result, sink_msg = verify_and_ingest_packet(sealed_packet)
    if result == "COMMITTED":
        print(f"\033[38;5;44m[✓] SINK RESOLUTION: {result}\033[0m")
        print(f"    └── {sink_msg}")
    else:
        print(f"\033[38;5;214m[✕] SINK RESOLUTION: {result}\033[0m")
        print(f"    └── {sink_msg}")
    print("="*90)

if __name__ == "__main__":
    run_integration_pipeline()
