#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template
from flask_babel import Babel
from typing import Tuple

app = Flask(__name__)
bebel = Babel(app)

app_views = Blueprint('app_views', __name__, url_prefix='/')


@app_views.route('/', strict_slashes=False)
def home() -> Tuple[str, int]:
    """ Home page """
    return render_template('1-index.html'), 200


app.register_blueprint(app_views)


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
