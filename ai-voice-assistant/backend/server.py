#issue tokens to frontend for each room creation
import os
from livekit import api
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from livekit.api import LiveKitAPI, ListRoomsRequest
import uuid

load_dotenv()

app = Flask(__name__)
#allow any other domain to access backend
CORS(app, resources={r"/*": {"origins": "*"}})

async def generate_room_name():
    #unique id
    name = "room-" + str(uuid.uuid4())[:8]
    #makes sure room is unique - name is random
    rooms = await get_rooms()
    while name in rooms:
        name = "room-" + str(uuid.uuid4())[:8]
    return name

#finds currently active rooms
async def get_rooms():
    api = LiveKitAPI
    rooms = await api.room.list_rooms(ListRoomsRequest)
    await api.aclose()
    return [room.name for room in rooms.rooms]

#issues new token to allow user to connect to new room
@app.route("/getToken")
def get_token():
    try:
        name = request.args.get("name", "my name")
        room = request.args.get("room", None)

        if not room: 
            room = generate_room_name()
        
        key = os.getenv("LIVEKIT_API_KEY")
        secret = os.getenv("LIVEKIT_API_SECRET")

        if not key or not secret:
            return jsonify({"error": "Missing LiveKit API key or secret"}), 500

        token = api.AccessToken(key, secret).with_identity(name)\
            .with_name(name)\
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room
            ))
        
        return token.to_jwt()
    except Exception as e:
        print(f"Error in /getToken: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
