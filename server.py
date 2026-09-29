import http.server
import json
import sqlite3
from datetime import datetime

# 🗄️ 1. ARCHITECT AND INITIALIZE COLD-STORAGE DATABASE RELATIONAL TABLES
def initialize_database():
    conn = sqlite3.connect("sovereignty.db")
    cursor = conn.cursor()
    
    # Permanent Focus Hours Archive Matrix
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_telemetry (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_vector TEXT NOT NULL,
            timestamp_marker TEXT NOT NULL,
            focus_node TEXT NOT NULL,
            duration_hours REAL NOT NULL,
            session_status TEXT NOT NULL,
            interruption_reason TEXT DEFAULT 'None'
        )
    """)
    
    # Permanent Health Log Archive Matrix
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_telemetry (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_vector TEXT NOT NULL,
            timestamp_marker TEXT NOT NULL,
            action_type TEXT NOT NULL,
            current_count INTEGER NOT NULL,
            safety_ceiling INTEGER DEFAULT 14
        )
    """)
    
    # Permanent Nutritional Guard Archive Matrix
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nutrition_ledger (
            meal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_vector TEXT NOT NULL,
            timestamp_marker TEXT NOT NULL,
            meal_type TEXT NOT NULL,
            food_description TEXT NOT NULL,
            acid_protection_status TEXT DEFAULT 'Protected'
        )
    """)
    
    conn.commit()
    conn.close()
    print("🎯 SYSTEM DB ENGINE CORE INITIALIZED: sovereignty.db is online and tracking.")

# Initialize database schemas before starting the listener runtime
initialize_database()

# 🔌 2. API ENDPOINT ROUTING ENGINE HANDLER
class SovereignAPIHandler(http.server.BaseHTTPRequestHandler):
    
    # Override CORS preflight rules to allow multi-device phone connections
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def send_json_response(self, status_code, data_dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data_dict).encode("utf-8"))
    # 📥 HANDLE POST DATA INCOMING FROM WEB Cockpit
    def do_POST(self):
        # Read the size of the payload content data line
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.wfile.read(content_length) if content_length > 0 else b""
        
        # Determine target API endpoint vector route path
        if self.path == "/api/study":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                conn = sqlite3.connect("sovereignty.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO study_telemetry 
                    (date_vector, timestamp_marker, focus_node, duration_hours, session_status, interruption_reason) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    payload.get("date_vector"),
                    payload.get("timestamp_marker"),
                    payload.get("focus_node"),
                    payload.get("duration_hours"),
                    payload.get("session_status"),
                    payload.get("interruption_reason", "None")
                ))
                conn.commit()
                conn.close()
                self.send_json_response(200, {"status": "SUCCESS", "message": "STUDY LOG COMMITTED TO DB"})
            except Exception as e:
                self.send_json_response(400, {"status": "ERROR", "message": str(e)})

        elif self.path == "/api/health":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                conn = sqlite3.connect("sovereignty.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO health_telemetry 
                    (date_vector, timestamp_marker, action_type, current_count, safety_ceiling) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    payload.get("date_vector"),
                    payload.get("timestamp_marker"),
                    payload.get("action_type"),
                    payload.get("current_count"),
                    payload.get("safety_ceiling", 14)
                ))
                conn.commit()
                conn.close()
                self.send_json_response(200, {"status": "SUCCESS", "message": "HEALTH TELEMETRY COMMITTED TO DB"})
            except Exception as e:
                self.send_json_response(400, {"status": "ERROR", "message": str(e)})

        elif self.path == "/api/nutrition":
            try:
                payload = json.loads(post_data.decode("utf-8"))
                conn = sqlite3.connect("sovereignty.db")
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO nutrition_ledger 
                    (date_vector, timestamp_marker, meal_type, food_description, acid_protection_status) 
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    payload.get("date_vector"),
                    payload.get("timestamp_marker"),
                    payload.get("meal_type"),
                    payload.get("food_description"),
                    payload.get("acid_protection_status", "Protected")
                ))
                conn.commit()
                conn.close()
                self.send_json_response(200, {"status": "SUCCESS", "message": "NUTRITION RECOVERY GUARD COMMITTED TO DB"})
            except Exception as e:
                self.send_json_response(400, {"status": "ERROR", "message": str(e)})
        else:
            self.send_json_response(404, {"status": "ERROR", "message": "ENDPOINT PATH NOT FOUND"})

    # 📤 HANDLE DATA FETCHING SYNCHRONIZATION FOR CLIENT DEVICES
    def do_GET(self):
        if self.path == "/api/sync":
            try:
                conn = sqlite3.connect("sovereignty.db")
                cursor = conn.cursor()
                
                # Fetch latest real-time vape puff counts line trace marker
                cursor.execute("SELECT current_count FROM health_telemetry ORDER BY log_id DESC LIMIT 1")
                row = cursor.fetchone()
                latest_vape = row[0] if row else 0
                
                # Fetch total focus hour cumulative summary trace
                cursor.execute("SELECT SUM(duration_hours) FROM study_telemetry")
                row_hours = cursor.fetchone()
                total_hours = row_hours[0] if row_hours[0] is not None else 0.0
                
                conn.close()
                self.send_json_response(200, {
                    "status": "SUCCESS", 
                    "latest_vape_count": latest_vape,
                    "total_study_hours": total_hours
                })
            except Exception as e:
                self.send_json_response(500, {"status": "ERROR", "message": str(e)})
        else:
            self.send_json_response(404, {"status": "ERROR", "message": "PATH NOT FOUND"})

# 📡 3. INITIALIZE INTEL NETWORK BOUNDARY LISTENER RUNLOOP
def run_server(port=8080):
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, SovereignAPIHandler)
    print(f"📡 SOVEREIGN NETWORK ENGINE ONLINE: Listening on port {port} 24/7...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server environment shutdown safely.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
