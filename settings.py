import re
from os import getenv
from string import ascii_letters, digits

CUSTOM_ID_LENGTH = 16
SYMBOLS = ascii_letters + digits
CUSTOM_ID_REGEX = re.compile(
    "^["
    + re.escape(SYMBOLS)
    + "]{1,"
    + str(CUSTOM_ID_LENGTH)
    + "}$"
)
REDIRECT_VIEW = 'redirect_view'
ORIGINAL_LINK_LENGTH = 256


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = getenv('SECRET_KEY')
