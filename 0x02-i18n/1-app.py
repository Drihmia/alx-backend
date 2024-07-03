#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, Blueprint, render_template
from flask_babel import Babel
from typing import Tuple

app = Flask(__name__)
bebel = Babel(app)


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def home() -> Tuple[str, int]:
    """ Home page """
    return render_template('1-index.html'), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
