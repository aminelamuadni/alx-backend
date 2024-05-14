#!/usr/bin/env python3
"""
This module simulates user login behavior in a Flask application,
selecting language and timezone preferences based on the user's settings.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ['en', 'fr', 'kg']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


def get_user():
    """
    Retrieve a user dictionary from the users table based on the 'login_as' URL
    parameter.
    """
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set the global user object before every request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Select a language translation to use based on the user settings or client
    request.
    """
    user_locale = getattr(g.user, 'locale', None) if g.user else None
    if user_locale and user_locale in app.config['LANGUAGES']:
        return user_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render a localized HTML template."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app
