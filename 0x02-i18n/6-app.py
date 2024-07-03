#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template, request, g
from flask_babel import Babel


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


app = Flask(__name__)


# @babel.locale_selector
def get_locale():
    """ Get locale from request """
    args = request.args
    if "locale" in args:
        locale = args.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale

    if "login_as" in args:
        user_id = args.get("login_as")
        if user_id and user_id.isnumeric():
            user_obj = users.get(int(user_id))
            if user_obj and isinstance(user_obj, dict):
                locale = user_obj.get('locale')
                if locale in app.config['LANGUAGES']:
                    return locale

    headers = request.headers

    if "locale" in headers:
        locale = headers.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ Get user from request """
    args = request.args
    if "login_as" in args:
        user_id = args.get("login_as")
        if user_id and user_id.isnumeric():
            return users.get(int(user_id))


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
babel = Babel(app, locale_selector=get_locale)

app_views = Blueprint('app_views', __name__, url_prefix='/')

# @app_views.before_request
@app_views.route('/', strict_slashes=False)
def home():
    return render_template('5-index.html'), 200


@app.before_request
def before_request():
    """ Before request """
    g.user = get_user()


app.register_blueprint(app_views)
# app.before_request(before_request)

if __name__ == "__main__":
    app.run()
