from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema


def validate_date(n):
    if n < 1:
        raise ValidationError('Number of date must be greater than 0.')

    if n > 31:
        raise ValidationError('Number of date must not be greater than 31.')

class RoomSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    date = fields.Integer(validate=validate_date)
    start_time = fields.Integer()
    duration = fields.String(validate=[validate.Length(max=1000)])

    is_publish = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):

        if many:
            return {'data': data}

        return data

    @validates('start_time')
    def validate_start_time(self, value):
        if value < 16:
            raise ValidationError('Start time must be greater than 16.')

        if value > 21:
            raise ValidationError('Start time must not be greater than 21.')

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, exclude=('email',))