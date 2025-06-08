import logging
from flask import Blueprint, redirect, render_template, request, url_for, abort
from sqlalchemy.exc import IntegrityError
from .database import db_session
from .models import Product


bp = Blueprint("inventory", __name__)
logging.basicConfig(level=logging.DEBUG)


@bp.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@bp.route("/", methods=["GET", "POST"])
def home():
    products = Product.query.all()
    logging.info("Showing all the products in the inventory")
    return render_template("crud/list.html", products=products)


@bp.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        mac_address = request.form["mac_address"]
        serial_number = request.form["serial_number"]
        manufacturer = request.form["manufacturer"]
        description = request.form["description"]
        product = Product(
            name=name,
            price=price,
            mac_address=mac_address,
            serial_number=serial_number,
            manufacturer=manufacturer,
            description=description,
        )
        try:
            db_session.add(product)
            db_session.commit()
            logging.info(f"Product {name} added!")
            return redirect(url_for("inventory.home"))
        except IntegrityError:
            logging.error(
                f"Duplited MAC Address {mac_address} or Serial number {serial_number}"
            )
            return (
                render_template(
                    "crud/create.html",
                    error="That MAC Address and/or serial number are duplicated.",
                ),
                409,
            )
    return render_template("crud/create.html")


@bp.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    product = db_session.get(Product, id)
    if product == None:
        abort(404)
    if request.method == "POST":
        db_session.delete(product)
        db_session.commit()
        logging.info(f"Product {product.name} has been deleted")
        return redirect(url_for("inventory.home"))
    return render_template("crud/delete.html", product=product)


@bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    product = db_session.get(Product, id)
    if product == None:
        abort(404)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = request.form["price"]
        product.mac_address = request.form["mac_address"]
        product.serial_number = request.form["serial_number"]
        product.manufacturer = request.form["manufacturer"]
        product.description = request.form["description"]
        db_session.commit()
        logging.info(f"Product {product.name} has been edited")
        return redirect(url_for("inventory.home"))
    return render_template("crud/edit.html", product=product)
