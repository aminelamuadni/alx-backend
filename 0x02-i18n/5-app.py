#!/usr/bin/env python3
"""
This module simulates user login behavior in a Flask application,
selecting language and timezone preferences based on the user's settings.
"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel, _


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False
app.config.from_object(Config)


def get_user() -> Union[Dict, None]:
    """
    Retrieve a user dictionary from the users table based on the 'login_as' URL
    parameter.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request() -> None:
    """Set the global user object before every request."""
    g.user = get_user()


@babel.localeselector
def get_locale() -> str:
    """
    Select a language translation to use based on the user settings or client
    request.
    """
    user_locale = request.args.get('locale')
    if user_locale in app.config['LANGUAGES']:
        return user_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """Render a localized HTML template."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app
