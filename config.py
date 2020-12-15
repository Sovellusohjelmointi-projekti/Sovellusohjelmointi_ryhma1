class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://admin:kiisu@localhost:5432/tuasreservations' #tätä pitää muuttaa!
    SQLALCHEMY_TRACK_MODIFICATIONS = False
