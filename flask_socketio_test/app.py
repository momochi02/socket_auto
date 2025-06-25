from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import subprocess, threading
from test_scripts import run_test_for_app

app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, cors_allowed_origins='*')
connected_devices = set()

# Track device via adb track-devices
def track_devices():
    process = subprocess.Popen(["adb", "track-devices"], stdout=subprocess.PIPE, text=True)
    for line in process.stdout:
        if "device" in line and not line.startswith("List"):
            serial = line.split()[0]
            if serial not in connected_devices:
                connected_devices.add(serial)
                print(f"Device connected: {serial}")
                socketio.emit("device_connected", {"serial": serial})
        elif "offline" in line:
            serial = line.split()[0]
            if serial in connected_devices:
                connected_devices.remove(serial)
                print(f"Device removed: {serial}")
                socketio.emit("device_removed", {"serial": serial})

@app.route("/")
def serve_index():
    return send_from_directory("static", "index.html")

@app.route("/devices")
def get_devices():
    return jsonify(list(connected_devices))

@app.route("/run-test", methods=["POST"])
def run_test():
    data = request.get_json()
    serial = data.get("serial")
    app_name = data.get("app")
    if not serial or not app_name:
        return jsonify({"error": "missing serial or app"}), 400

    def test_and_emit():
        result = run_test_for_app(app_name, serial)
        socketio.emit("test_result", result)

    threading.Thread(target=test_and_emit).start()
    return jsonify({"status": "started"})

@socketio.on("connect")
def on_connect():
    print("Client connected")
    emit("device_list", list(connected_devices))

if __name__ == "__main__":
    threading.Thread(target=track_devices, daemon=True).start()
    socketio.run(app, port=5000)
