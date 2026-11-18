#!/usr/bin/env python3
"""
Connext Media Office Backend
- Status file: status.json
- Token auth (simple shared secret)
- Rate limiting
"""
import json
import time
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict

app = Flask(__name__)
CORS(app)

STATUS_FILE = Path(__file__).parent / "status.json"
TOKEN = "connext-media-secret-token-2026"  # Change in production
RATE_LIMIT = 30  # requests per minute per IP
rate_store = defaultdict(list)

def load_status():
    if STATUS_FILE.exists():
        return json.loads(STATUS_FILE.read_text())
    return {"bots": [], "updated": ""}

def save_status(data):
    data["updated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    STATUS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))

def check_rate(ip):
    now = time.time()
    rate_store[ip] = [t for t in rate_store[ip] if now - t < 60]
    if len(rate_store[ip]) >= RATE_LIMIT:
        return False
    rate_store[ip].append(now)
    return True

@app.route("/api/status", methods=["GET"])
def get_status():
    return jsonify(load_status())

@app.route("/api/report", methods=["POST"])
def report():
    ip = request.remote_addr or "unknown"
    if not check_rate(ip):
        return jsonify({"error": "rate limited"}), 429

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != TOKEN:
        return jsonify({"error": "unauthorized"}), 401

    data = request.json or {}
    bot_id = data.get("id") or data.get("name", "").lower()
    status = data.get("status", "idle")
    task = data.get("task", "")

    db = load_status()
    found = False
    for bot in db.get("bots", []):
        if bot["id"] == bot_id or bot["name"].lower() == bot_id:
            bot["status"] = status
            bot["task"] = task
            found = True
            break
    if not found:
        return jsonify({"error": "bot not found"}), 404

    save_status(db)
    return jsonify({"ok": True, "bot": bot_id, "status": status})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "connext-office"})

if __name__ == "__main__":
    print("Starting Connext Media Office Backend on :5000")
    print(f"Token: {TOKEN}")
    app.run(host="0.0.0.0", port=5000, debug=False)
