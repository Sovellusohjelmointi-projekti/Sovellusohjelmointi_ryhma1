from extensions import db


class Room(db.Model):
    __tablename__ = 'room'

    room_list = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), nullable=False, unique=True)
    available = db.Column(db.String(80), nullable=False, unique=False)

    @classmethod
    def get_by_room_name(cls, room_name):
        return cls.query.filter_by(room_name=room_name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()


class RoomList(db.Model):
    __tablename__ = 'room_list'

    room_list = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(80), nullable=False, unique=True)
    available = db.Column(db.String(80), nullable=False, unique=False)

    @classmethod
    def get_by_room_name(cls, room_name):
        return cls.query.filter_by(room_name=room_name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()