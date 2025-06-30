# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename


# stdlib
from datetime import datetime
import os

# local





from .stats.routes import stats

def custom_404(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_pyfile("config.py", silent=False)
    if test_config is not None:
        app.config.update(test_config)

    app.register_blueprint(stats) 

    app.register_error_handler(404, custom_404)

    return app
