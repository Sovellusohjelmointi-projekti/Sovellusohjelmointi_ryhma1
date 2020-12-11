from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask import request
from http import HTTPStatus
from flask_restful import Resource
from models.user import User  # tämä tarkastaa että on samassa paikassa, tuskin on
from utils import hash_password  # tämä vielä tekemättä!


class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if current_user == user.id:

            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        else:

            data = {
                'id': user.id,
                'username': user.username
            }

        return data, HTTPStatus.OK
