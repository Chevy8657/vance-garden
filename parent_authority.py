#!/usr/bin/env python3
import http.server
import json
import sqlite3
import hashlib
import time

PORT = 3000
DB_FILE = "district.db"
SHARED_SECRET = "farm_bureau_national_compliance_secret_key"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT,
            timestamp INTEGER,
            status TEXT,
            load_avg TEXT,
            uptime INTEGER
        )
    """)
    conn.commit()
    conn.close()

class ParentAuthorityHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args): return

    def do_POST(self):
        if self.path == "/api/telemetry":
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            provided_token = self.headers.get("X-District-Token", "")
            
            try:
                payload = json.loads(body.decode('utf-8'))
                node_id = payload.get("node_id")
                timestamp = payload.get("timestamp")
                
                if abs(int(time.time()) - int(timestamp)) > 60:
                    self.send_response(401)
                    self.end_headers()
                    self.wfile.write(b"Rejected: Telemetry window expired.")
                    return

                hasher = hashlib.sha256()
                hasher.update(f"{SHARED_SECRET}{node_id}{timestamp}".encode('utf-8'))
                expected_token = hasher.hexdigest()
                
                if provided_token != expected_token:
                    self.send_response(403)
                    self.end_headers()
                    self.wfile.write(b"Rejected: Signature mismatch.")
                    return
                
                metrics = payload.get("metrics", {})
                load_str = str(metrics.get("load_avg", [0,0,0]))
                uptime = metrics.get("uptime", 0)
                
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO telemetry_ledger (node_id, timestamp, status, load_avg, uptime)
                    VALUES (?, ?, ?, ?, ?)
                """, (node_id, timestamp, payload.get("status"), load_str, uptime))
                conn.commit()
                conn.close()
                
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Verified & Committed")
                
            except Exception as e:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"Error processing packet: {str(e)}".encode())

if __name__ == "__main__":
    init_db()
    server = http.server.HTTPServer(("0.0.0.0", PORT), ParentAuthorityHandler)
    print(f"🛡️  V.A.N.C.E. Parent Authority active on Port {PORT} [CRYPTO ENFORCED]")
    try: server.serve_forever()
    except KeyboardInterrupt: print("\n🛑 Parent Authority safely offline.")
