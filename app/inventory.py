from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from .database import db_session
from .models import Product

bp = Blueprint('inventory', __name__)


@bp.route("/")
def home():
    products = Product.query.all()
    return render_template("crud/list.html",products = products)

@bp.route("/add")
def create():
    return render_template("crud/create.html")
    
@bp.route("/add-request",methods = ['POST'])
def add_request():
    name = request.form["name"]
    mac_address = request.form["mac_address"]
    serial_number = request.form["serial_number"]
    manufacturer = request.form["manufacturer"]
    description = request.form["description"]

    product = Product(name=name, mac_address=mac_address,serial_number=serial_number,manufacturer=manufacturer,description=description)
    db_session.add(product)
    db_session.commit()

    return redirect(url_for('home'))