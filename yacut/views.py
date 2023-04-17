from flask import render_template, flash, url_for, redirect

from . import app, db
from .form import URLForm
from .models import URLMap
from .utils import get_unique_short_id, check_uniqueness_short_id

@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    if check_uniqueness_short_id(custom_id) is not None:
        flash(f'Короткая ссылка {custom_id} занята')
        return render_template('index.html', form=form)
    url = URLMap(
        original = form.original_link.data,
        short = custom_id
    )
    db.session.add(url)
    db.session.commit()
    flash(url_for('redirect_view', short=custom_id, _external=True))
    return render_template('index.html', url=url, form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
