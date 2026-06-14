import json
import os
import time

EGRESS_SPOOL_PATH = '/home/rick/pet_alpha/egress_spool.json'
TRANSMIT_LOG_PATH = '/home/rick/pet_alpha/broadcast_history.log'

class CoreBroadcastDaemon:
    def __init__(self):
        # Establish targeted routing matrices for our primary technological infrastructure hubs
        self.routing_registry = {
            "REGISTRY-BRK-9922": ["NODE-NEVADA-001", "NODE-TEXAS-099", "NODE-FLORIDA-007"]
        }

    def process_egress_spool(self):
        """
        Pulls staged packets from the spool, resolves physical network routing targets,
        and flushes the wire queue safely.
        """
        print("="*90)
        print("INITIALIZING OUTBOUND NETWORK BROADCAST DAEMON RUN")
        print("="*90)

        if not os.path.exists(EGRESS_SPOOL_PATH):
            print("[i] Egress network spool is currently pristine. Zero pending packets.")
            print("="*90)
            return

        try:
            with open(EGRESS_SPOOL_PATH, 'r') as f:
                pending_packets = json.load(f)
        except (json.JSONDecodeError, ValueError):
            print("\033[38;5;196m[✕] DAEMON CRITICAL: Spool corrupt or unreadable.\033[0m")
            print("="*90)
            return

        if not pending_packets:
            print("[i] Spool queue contains empty array. Standing down broadcast hardware.")
            print("="*90)
            return

        print(f"[➔] Found {len(pending_packets)} pending transit envelope(s) ready for broadcast.\n")
        
        processed_ids = []

        for packet in pending_packets:
            pkt_id = packet.get("outbound_packet_id")
            payload = json.loads(packet.get("serialized_payload", "{}"))
            context = payload.get("routing_context")
            
            # Resolve physical network destinations
            destinations = self.routing_registry.get(context, ["NODE-UNKNOWN-EDGE"])
            print(f"[📡 BROADCASTING] Packet ID: {pkt_id} -> Context: {context}")
            
            for node in destinations:
                # Simulating isolated asynchronous wire delivery
                time.sleep(0.1) 
                print(f"    └── ➔ Transmitted to peer endpoint: \033[38;5;44m{node}\033[0m [STATUS: 200 OK]")
            
            processed_ids.append(pkt_id)

        # Atomic Queue Cleanup: Flush only what we successfully broadcasted
        remaining_packets = [p for p in pending_packets if p.get("outbound_packet_id") not in processed_ids]
        
        with open(EGRESS_SPOOL_PATH, 'w') as f:
            json.dump(remaining_packets, f, indent=4)

        # Log completion to persistent daemon history
        with open(TRANSMIT_LOG_PATH, 'a') as log_f:
            for pid in processed_ids:
                log_f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Broadcast Complete: {pid}\n")

        print(f"\n\033[38;5;44m[✓] Queue Sync Successful: {len(processed_ids)} packets flushed from spool.\033[0m")
        print("="*90)

if __name__ == "__main__":
    daemon = CoreBroadcastDaemon()
    daemon.process_egress_spool()
