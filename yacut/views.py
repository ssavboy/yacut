from flask import flash, redirect, render_template, url_for

from . import app, db
from .form import URLForm
from .models import URLMap
from .utils import check_uniqueness_short_id, get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    if check_uniqueness_short_id(custom_id) is None:
        flash(f'Имя {custom_id} уже занято!', 'info')
        return render_template('index.html', form=form)
    url = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url)
    db.session.commit()
    flash(url_for('redirect_view', short=custom_id, _external=True), 'custom_id')
    return render_template('index.html', url=url, form=form)


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
