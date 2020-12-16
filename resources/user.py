from flask import request, url_for
from flask_restful import Resource
from http import HTTPStatus

from mailgun import MailGunApi

from utils import generate_token, verify_token

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.room import Room
from models.user import User

from schemas.room import RoomSchema
from schemas.user import UserSchema

from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required

mailgun = MailGunApi(domain='sandbox9be86adbecee46cb9cc4b6091e029175.mailgun.org', api_key='3ec268486f6770bb4f8a9f147fa227b3-e5da0167-69e770d9')

user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

room_list_schema = RoomSchema(many=True)

class UserListResource(Resource):

    def post(self):
        json_data = request.get_json()

        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors.', 'errors': errors}, HTTPStatus.BAD_REQUEST

        if User.get_by_username(data.get('username')):
            return {'message': 'Username already used.'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'Email already used.'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        token = generate_token(user.email, salt='activate')
        subject = 'Please confirm your registration.'

        link = url_for('useractivateresource',
                       token=token,
                       _external=True)
        text = 'Hi, Thanks for using TUASreservations! Please confirm your registration by clicking on the link: {}'.format(link)
        mailgun.send_email(to=user.email,
                           subject=subject,
                           text=text)

        return user_schema.dump(user).data, HTTPStatus.CREATED

class UserResource(Resource):

    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data

        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK

class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK

class UserRoomListResource(Resource):

    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        rooms = Room.get_all_by_user(user_id=user.id, visibility=visibility)

        return room_list_schema.dump(rooms).data, HTTPStatus.OK

class UserActivateResource(Resource):
    def get(self, token):

        email = verify_token(token, salt='activate')

        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True
        user.save()

        return {}, HTTPStatus.NO_CONTENT
