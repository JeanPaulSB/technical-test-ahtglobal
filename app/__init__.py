import os
import logging
from flask import Flask, render_template, redirect, url_for, request
from .database import init_db, db_session
from .models import Product

logging.basicConfig(level=logging.DEBUG)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    init_db()

    from . import inventory
    app.register_blueprint(inventory.bp)
    app.add_url_rule('/', endpoint='index')


    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
