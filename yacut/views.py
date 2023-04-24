from flask import flash, redirect, render_template, url_for

from . import app
from .exceptions import (IncorrectOriginalException, IncorrectShortException,
                         NonUniqueException)
from .form import URLForm
from .models import URLMap
from settings import REDIRECT_VIEW

FLASH_MESSAGE = 'Имя {} уже занято.'


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
                    form.custom_id.data,
                    is_validate=False
                ).short,
                _external=True
            )
        )
    except IncorrectOriginalException as error:
        flash(error)
    except IncorrectShortException as error:
        flash(error)
    except NonUniqueException:
        flash(FLASH_MESSAGE.format(URLMap.short))


@app.route('/<string:short>', methods=['GET'])
def redirect_view(short):
    return redirect(
        URLMap.get_or_404(short)
    )
