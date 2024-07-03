#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template, request
from flask_babel import Babel

app = Flask(__name__)


# @babel.locale_selector
def get_locale():
    """ Get locale from request """
    args = request.args
    if "locale" in args and args.get('locale') in app.config['LANGUAGES']:
        return args.get('locale')
    return request.accept_languages.best_match(app.config['LANGUAGES'])


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app, locale_selector=get_locale)

app_views = Blueprint('app_views', __name__, url_prefix='/')


@app_views.route('/', strict_slashes=False)
def home():
    """ Home page """
    return render_template('4-index.html'), 200


app.register_blueprint(app_views)


if __name__ == "__main__":
    app.run(debug=True)
