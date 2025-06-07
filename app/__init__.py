import os
import logging
from flask import Flask,render_template
from .database import init_db, db_session
from .models import Product

logging.basicConfig(level=logging.DEBUG)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    init_db()

    @app.route("/")
    def home():
        logging.debug(Product.query.all())
        logging.debug("hey")
        return render_template("crud/list.html")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app
