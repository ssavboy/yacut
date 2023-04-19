from random import choices
from string import ascii_letters, digits

from .models import URLMap


def get_unique_short_id():
    while True:
        symbols = ascii_letters + digits
        unique_short_id = ''.join(choices(symbols, k=6))
        if not URLMap.query.filter_by(short=unique_short_id).first():
            return unique_short_id


def check_uniqueness_short_id(custom_id):
    if URLMap.query.filter_by(short=custom_id).first():
        return None
    return custom_id
