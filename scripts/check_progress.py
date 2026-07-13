#!/usr/bin/env python3
import sqlite3
import json
import os

DB_FILE = "npm_ecosystem.db"
STATE_FILE = "last_notified.json"

def main():
    if not os.path.exists(DB_FILE):
        print("SILENT: DB does not exist yet.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Count completed scrapes
    cursor.execute("SELECT COUNT(*) FROM packages WHERE fetched_registry = 1 AND fetched_dependencies = 1")
    current_count = cursor.fetchone()[0]
    conn.close()
    
    last_notified = 0
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                last_notified = data.get("last_notified", 0)
        except Exception:
            pass
            
    current_thousands = current_count // 1000
    last_thousands = last_notified // 1000
    
    if current_thousands > last_thousands:
        new_notified = current_thousands * 1000
        with open(STATE_FILE, "w") as f:
            json.dump({"last_notified": new_notified}, f)
        print(f"NOTIFICATION: {current_count}")
    else:
        print(f"SILENT: {current_count} (last notified {last_notified})")

if __name__ == "__main__":
    main()
