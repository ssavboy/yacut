from os import getenv


class Config(object):
    SQLALCHEMY_DATABASE_URI=getenv('DATABASE')
    SQLALCHEMY_TRACK_MODIFICATIONS=getenv('TRACK_MODIFICATION')
    SECRET_KEY=getenv('SECRET_KEY')