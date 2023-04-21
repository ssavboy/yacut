from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsageError
from .models import URLMap

EMPTY_BODY_REQUEST = 'Отсутствует тело запроса'
URL_REQUIRED_FIELD = '"url" является обязательным полем!'


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError(EMPTY_BODY_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsageError(URL_REQUIRED_FIELD)
    custom_id = data.get('custom_id')
    url_map = URLMap.micro_orm(data, custom_id)
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.get_short(short)
    if url_map is None:
        raise InvalidAPIUsageError('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200
