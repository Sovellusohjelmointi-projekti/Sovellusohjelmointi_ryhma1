class Config:
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://Admin:kiisu@localhost/TUASreservations'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = 'kiisu'
    JWT_ERROR_MESSAGE_KEY = 'message'

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']