from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import json
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

DATA_FILE = 'data.json'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/live-matches")
def api():
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"matches": []}), 500

def push_updates(interval=10):
    while True:
        try:
            with open(DATA_FILE) as f:
                data = json.load(f)
            socketio.emit("match_update", data)
        except:
            pass
        time.sleep(interval)

if __name__ == "__main__":
    threading.Thread(target=push_updates, daemon=True).start()
    socketio.run(app, port=5000, debug=True)
