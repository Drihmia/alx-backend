#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union, Tuple


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)


def get_user() -> Union[Dict[str, str],  None]:
    """ Returns a user dictionary or None if not found """
    args = request.args
    if "login_as" in args:
        user_id = args.get("login_as")
        if user_id and user_id.isnumeric():
            obj = users.get(int(user_id))
            if obj and isinstance(obj, dict):
                return obj
    return None


class Config:
    """ Babel configuration class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app)


@babel.locale_selector
def get_locale() -> str:
    """ Determine the best match for supported languages """
    args = request.args
    if "locale" in args:
        locale = args.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


app_views = Blueprint('app_views', __name__, url_prefix='/')

# @app_views.before_request
@app_views.route('/', strict_slashes=False)
def home() -> Tuple[str, int]:
    """ Returns a simple HTML page """
    return render_template('5-index.html'), 200


@app.before_request
def before_request():
    """ Executed before all request """
    g.user = get_user()


app.register_blueprint(app_views)
# app.before_request(before_request)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
