from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

processed_rooms = {}

EXPIRATION_SECONDS = 600

@app.route('/addroom', methods=['POST'])
def add_room():
    data = request.get_json()
    if not data or 'room' not in data:
        return jsonify({"error": "Missing 'room' in JSON"}), 400

    room = data['room'].strip().upper()
    now = time.time()
    if room not in processed_rooms:
        processed_rooms[room] = now
        return jsonify({"message": f"Room '{room}' added", "roomlist": list(processed_rooms.keys())})
    else:
        return jsonify({"message": f"Room '{room}' already exists"}), 200

@app.route('/removeroom', methods=['POST'])
def remove_room():
    data = request.get_json()
    if not data or 'room' not in data:
        return jsonify({"error": "Missing 'room' in JSON"}), 400

    room = data['room'].strip().upper()
    if room in processed_rooms:
        del processed_rooms[room]
        return jsonify({"message": f"Room '{room}' removed", "roomlist": list(processed_rooms.keys())})
    else:
        return jsonify({"error": f"Room '{room}' not found"}), 404

@app.route('/roomlist', methods=['GET'])
def get_room_list():
    return jsonify({"rooms": list(processed_rooms.keys())})

def cleanup_rooms():
    while True:
        now = time.time()
        expired = [room for room, added_time in processed_rooms.items() if now - added_time > EXPIRATION_SECONDS]
        for room in expired:
            print(f"[CLEANUP] Removing expired room: {room}")
            del processed_rooms[room]
        time.sleep(60)

def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=cleanup_rooms, daemon=True).start()
    threading.Thread(target=run_flask).start()