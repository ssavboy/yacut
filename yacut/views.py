from flask import flash, redirect, render_template, url_for

from settings import REDIRECT_VIEW

from . import app
from .exceptions import (IncorrectOriginalException, IncorrectShortException,
                         NonUniqueException)
from .form import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=url_for(
                REDIRECT_VIEW,
                short=URLMap.create(
                    form.original_link.data,
                    form.custom_id.data
                ).short,
                _external=True
            )
        )
    except (IncorrectOriginalException, IncorrectShortException, NonUniqueException):
        flash(f'Имя {form.custom_id.data} уже занято.')


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.get_or_404(short)
    )
