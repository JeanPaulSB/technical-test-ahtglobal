from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from .database import db_session
from .models import Product
import logging

bp = Blueprint("inventory", __name__)
logging.basicConfig(level=logging.DEBUG)


@bp.route("/", methods=["GET", "POST"])
def home():
    products = Product.query.all()
    return render_template("crud/list.html", products=products)


@bp.route("/add", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        mac_address = request.form["mac_address"]
        serial_number = request.form["serial_number"]
        manufacturer = request.form["manufacturer"]
        description = request.form["description"]
        product = Product(
            name=name,
            mac_address=mac_address,
            serial_number=serial_number,
            manufacturer=manufacturer,
            description=description,
        )
        db_session.add(product)
        db_session.commit()
        return redirect(url_for("inventory.home"))
    return render_template("crud/create.html")


@bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        id = request.form["id"]
        product = Product.query.get(id)
        logging.info(product)
        if product:
            db_session.delete(product)
            db_session.commit()
            return redirect(url_for("inventory.home"))

    product = Product.query.get(id)
    return render_template("crud/delete.html", product=product)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    product = Product.query.get(id)
    return render_template("crud/edit.html", product=product)
