#!/usr/bin/env python3
"""
This module configures a Flask application to determine the preferred locale
from multiple sources with a specified priority order.
"""

from typing import Dict, Union
from flask import Flask, render_template, request, g
from flask_babel import Babel


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app."""
    DEBUG = True
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)
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
    # Extract 'locale' from query parameters
    query_locale = request.args.get('locale')
    if query_locale and query_locale in app.config['LANGUAGES']:
        return query_locale

    # Check if user is logged in and has a locale set
    user = getattr(g, 'user', None)
    if user and user.get('locale') in app.config['LANGUAGES']:
        return user['locale']

    # Extract 'locale' from headers
    header_locale = request.headers.get('locale')
    if header_locale and header_locale in app.config['LANGUAGES']:
        return header_locale

    # Default to the configured default locale
    return app.config['BABEL_DEFAULT_LOCALE']


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render a localized HTML template."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
