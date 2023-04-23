from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .exceptions import IncorrectShortException, NonUniqueException
from .models import INCORRECT_NAME_SHORT_URL, NAME_ALREADY_EXISTS, URLMap

EMPTY_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError(EMPTY_BODY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsageError(URL_REQUIRED_FIELD)
    try:
        url = URLMap.create_url_object(
            data.get('url'),
            data.get('custom_id')
        )
    except IncorrectShortException:
        raise InvalidAPIUsageError(INCORRECT_NAME_SHORT_URL, 400)
    except NonUniqueException:
        raise InvalidAPIUsageError(
            NAME_ALREADY_EXISTS.format(
                data.get('custom_id')
            ), 400
        )
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get_short(short)
    if url_map is None:
        raise InvalidAPIUsageError('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
