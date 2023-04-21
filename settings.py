from os import getenv
from string import ascii_letters, digits

redirect_view = 'redirect_view'
symbols = ascii_letters + digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
