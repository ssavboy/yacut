from re import match

from flask import jsonify, request

from . import app, db
from .const import LENGTH, PATTERN
from .error_handlers import InvalidAPIUsageError
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_id():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsageError('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsageError('"url" является обязательным полем!')
    custom_id = data.get('custom_id')
    if 'custom_id' not in data or custom_id is None:
        data['custom_id'] = get_unique_short_id()
    if custom_id:
        if URLMap.query.filter_by(short=custom_id).first() is not None:
            raise InvalidAPIUsageError(f'Имя "{custom_id}" уже занято.',)
        if not match(PATTERN, custom_id) or len(custom_id) > LENGTH:
            raise InvalidAPIUsageError('Указано недопустимое имя для короткой ссылки')
    urlmap = URLMap()
    urlmap.from_dict(data)
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(urlmap.to_dict()), 201


@app.route('/api/id/<string:short>/', methods=['GET'])
def get_url(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        raise InvalidAPIUsageError('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200