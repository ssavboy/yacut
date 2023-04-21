from flask import redirect, render_template, url_for

from . import app, db
from .form import URLForm
from .models import URLMap

ALREADY_TAKEN = 'Имя {} уже занято!'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    # Не могу сообразить как перенести проверки, при этом сохранить универсальность
    if not custom_id:
        custom_id = URLMap.get_unique_short_id()
    if URLMap.check_uniqueness_short_id(custom_id):
        return render_template(
            'index.html',
            form=form,
            already_taken_message=ALREADY_TAKEN.format(custom_id)
        )
    url = URLMap(
        original=form.original_link.data,
        short=custom_id
    )
    db.session.add(url)
    db.session.commit()

    return render_template(
        'index.html',
        url=url,
        form=form,
        new_link_ready_message=url_for(
            'redirect_view',
            short=custom_id,
            _external=True
        )
    )


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.get_short_or_404(short)
    )
