#!/usr/bin/env python3
"""
This module configures a Flask application with Flask-Babel to determine the
preferred locale from the client request.
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/', strict_slashes=False)
def index():
    """Render a basic HTML template."""
    return render_template('2-index.html')


@babel.localeselector
def get_locale() -> str:
    """Select a language translation to use based on the client request."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
