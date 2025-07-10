from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

processed_rooms = []

@app.route('/addroom', methods=['POST'])
def add_room():
    data = request.get_json()
    if not data or 'room' not in data:
        return jsonify({"error": "Missing 'room' in JSON"}), 400

    room = data['room'].strip().upper()
    if room not in processed_rooms:
        processed_rooms.append(room)
        return jsonify({"message": f"Room '{room}' added", "roomlist": processed_rooms})
    else:
        return jsonify({"message": f"Room '{room}' already exists"}), 200

@app.route('/removeroom', methods=['POST'])
def remove_room():
    data = request.get_json()
    if not data or 'room' not in data:
        return jsonify({"error": "Missing 'room' in JSON"}), 400

    room = data['room'].strip().upper()
    if room in processed_rooms:
        processed_rooms.remove(room)
        return jsonify({"message": f"Room '{room}' removed", "roomlist": processed_rooms})
    else:
        return jsonify({"error": f"Room '{room}' not found"}), 404

@app.route('/roomlist', methods=['GET'])
def get_room_list():
    return jsonify({"rooms": processed_rooms})

def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()