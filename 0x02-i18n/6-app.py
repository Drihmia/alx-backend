#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template, request, g
from flask_babel import Babel
from typing import Dict, Union


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """ Get locale from request """
    args = request.args
    if "locale" in args and isinstance(args, dict):
        locale = args.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    user_obj = get_user()
    if user_obj and isinstance(user_obj, dict):
        locale = user_obj.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    headers = request.headers

    if "locale" in headers and isinstance(headers, dict):
        locale = headers.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[Dict[str, str],  None]:
    """ Get user from request """
    args = request.args
    if "login_as" in args and isinstance(args, dict):
        user_id = args.get("login_as")
        if user_id and user_id.isnumeric():
            obj = users.get(int(user_id))
            if obj and isinstance(obj, dict):
                return obj
    return None


class Config:
    """ Config class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

app_views = Blueprint('app_views', __name__, url_prefix='/')

# @app_views.before_request
@app_views.route('/', strict_slashes=False)
def home() -> str:
    return render_template('6-index.html')


@app.before_request
def before_request():
    """ Before request """
    g.user = get_user()


app.register_blueprint(app_views)
# app.before_request(before_request)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
