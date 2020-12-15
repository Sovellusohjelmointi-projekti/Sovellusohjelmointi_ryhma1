from flask import request
from flask_restful import Resource
from http import HTTPStatus

<<<<<<< HEAD
from models.room import Room, room_list
=======
from models.room import Room
from schemas.room import RoomSchema

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

room_schema = RoomSchema()
room_list_schema = RoomSchema(many=True)
>>>>>>> Joonan


class RoomListResource(Resource):

    def get(self):

<<<<<<< HEAD
        data = []

        for room in room_list:
            if room.is_publish is True:
                data.append(room.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        room = Room(name=data['name'],
                        description=data['description'],
                        date=data['date'],
                        startTime=data['startTime'],
                        duration=data['duration'],)

        room_list.append(Room)

        return Room.data, HTTPStatus.CREATED


class RoomResource(Resource):

    def get(self, room_id):
        room = next((room for room in room_list if room.id == room_id and room.is_publish == True), None)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        return room.data, HTTPStatus.OK

    def put(self, room_id):
        data = Room.get_json()

        room = next((room for room in room_list if room.id == room_id), None)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room.name = data['name']
        room.description = data['description']
        room.date = data['date']
        room.start_time = data['start_time']
        room.duration = data['duration']

        return room.data, HTTPStatus.OK

    def delete(self, room_id):
        room = next((room for room in room_list if room.id == room_id), None)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room_list.remove(room)

        return {}, HTTPStatus.NO_CONTENT


class RoomPublishResource(Resource):

    def put(self, room_id):
        room = next((room for room in room_list if room.id == room_id), None)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, room_id):
        room = next((room for room in room_list if room.id == room_id), None)

        if room is None:
            return {'message': 'room not found'}, HTTPStatus.NOT_FOUND

        room.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
=======
        rooms = Room.get_all_published()

        return room_list_schema.dump(rooms).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = room_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors.", 'errors': errors}, HTTPStatus.BAD_REQUEST

        room = Room(**data)
        room.user_id = current_user
        room.save()

        return room_schema.dump(room).data, HTTPStatus.CREATED

    @jwt_required
    def patch(self, room_id):

        json_data = request.get_json()

        data, errors = room_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors.', 'errors': errors}, HTTPStatus.BAD_REQUEST

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.name = data.get('name') or room.name
        room.description = data.get('description') or room.description
        room.date = data.get('date') or room.date
        room.start_time = data.get('start_time') or room.start_time
        room.duration = data.get('duration') or room.duration

        room.save()

        return room_schema.dump(room).data, HTTPStatus.OK

class RoomResource(Resource):

    @jwt_optional
    def get(self, room_id):
        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if room.is_publish == False and room.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return room_schema.dump(room).data, HTTPStatus.OK

    @jwt_required
    def put(self, room_id):

        json_data = request.get_json()

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.name = json_data['name']
        room.description = json_data['description']
        room.date = json_data['date']
        room.start_time = json_data['start_time']
        room.duration = json_data['duration']

        room.save()

        return room.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.delete()

        return {}, HTTPStatus.NO_CONTENT

class RoomPublishResource(Resource):

    @jwt_required
    def put(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.is_publish = True
        room.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.is_publish = False
        room.save()

        return {}, HTTPStatus.NO_CONTENT
>>>>>>> Joonan
