#!/usr/bin/env python3
"""
This module configures a Flask application with Flask-Babel for
internationalization, using gettext to parameterize templates.
"""

from flask import Flask, render_template
from flask_babel import Babel, _


class Config:
    """Configuration class for Flask app."""
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """Select a language translation to use based on the client request."""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Render a localized HTML template."""
    return render_template('3-index.html', title=_("home_title"),
                           header=_("home_header"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
