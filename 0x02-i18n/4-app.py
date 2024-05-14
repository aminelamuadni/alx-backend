#!/usr/bin/env python3
"""
This module configures a Flask application with Flask-Babel for
internationalization, including a URL parameter to force a particular locale.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False
app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Select a language translation to use based on the client request or URL
    parameter.
    """
    user_locale = request.args.get('locale')
    if user_locale and user_locale in app.config['LANGUAGES']:
        return user_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render a localized HTML template."""
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
