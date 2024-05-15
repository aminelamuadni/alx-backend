#!/usr/bin/env python3
"""
This module configures a Flask application to determine the appropriate
timezone from multiple sources with validation using pytz.
"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


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
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


def get_user() -> Union[Dict, None]:
    """
    Retrieve a user dictionary from the users table based on the 'login_as' URL
    parameter.

    Returns:
        Union[Dict, None]: A dictionary representing the user if found, None
        otherwise.
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

    Returns:
        str: The selected language translation to use.
    """
    user_locale = request.args.get('locale')
    if user_locale in app.config['LANGUAGES']:
        return user_locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """
    Select a timezone to use based on multiple sources, validated with pytz.

    Returns:
        str: The selected timezone.

    Raises:
        UnknownTimeZoneError: If the provided timezone is unknown.
    """
    tz_url = request.args.get('timezone', '').strip()
    if not tz_url and g.user:
        tz_url = g.user['timezone']
    try:
        return pytz.timezone(tz_url).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/')
def index() -> str:
    """Render a localized HTML template."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
