#!/usr/bin/env python3
""" This module contains basic Flask app setup """
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    """ Config class """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
bebel = Babel(app)


@app.route('/')
def home() -> str:
    """ Home page """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
