from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.room import Room
from schemas.room import RoomSchema

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

room_schema = RoomSchema()
room_list_schema = RoomSchema(many=True)

class RoomListResource(Resource):

    def get(self):

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