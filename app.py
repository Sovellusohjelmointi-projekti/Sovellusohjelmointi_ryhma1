from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

rooms = [
    {
         "id": "1",
         "name": "Alpha",
         "description": "Auditorium",
         "date": "",
         "startTime": "",
         "duration": ""
    },
    {
        "id": "2",
        "name": "Beta",
        "description": "Auditorium",
        "date": "",
        "startTime": "",
        "duration": ""
    }
]

@app.route('/roomreservation', methods=['GET'])
def get_rooms():
    return jsonify({'data': rooms})

@app.route('/roomreservation/<int:room_id>', methods=['GET'])
def get_room(room_id):
    room = next((room for room in rooms if room['id'] == room_id), None)

    if room:
        return jsonify(room)

    return jsonify({'message': 'Room not found.'}), HTTPStatus.NOT_FOUND

@app.route('/roomreservation', methods=['POST'])
def create_room():
    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    date = data.get('date')
    startTime = data.get('startTime')
    duration = data.get('duration')
    room = {
        'id': len(rooms) + 1,
        'name': name,
        'date': data,
        'startTime': startTime,
        'duration': duration
    }

    rooms.append(room)

    return jsonify(room), HTTPStatus.CREATED

@app.route('/roomreservation/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = next((room for room in rooms if room['id'] == room_id), None)

    if not room:
        return jsonify({'message': 'Room not found.'}), HTTPStatus.NOT_FOUND

    data = request.get_json()

    room.update(
        {
            'name': data.get('name'),
            'date': data.get('date'),
            'startTime': data.get('startTime'),
            'duration': data.get('duration')
        }
    )

    return jsonify(room)

if __name__ == '__main__':
    app.run()