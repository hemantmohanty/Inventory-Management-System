from flask import Blueprint, render_template, redirect, request, url_for, flash
from app import db
from app.models import Customer, PriceGroup, Product, Warehouse, StockLedger, SalesOrder, WarehouseLocation

edit_bp = Blueprint("edit", __name__)

# ------ CUSTOMER ------
@edit_bp.route("/customer/delete/<int:id>")
def delete_customer(id):
    cust = Customer.query.get_or_404(id)
    db.session.delete(cust)
    db.session.commit()
    return redirect(url_for("dashboard.customer"))

@edit_bp.route("/customer/edit/<int:id>", methods=["GET", "POST"])
def edit_customer(id):
    cust = Customer.query.get_or_404(id)
    if request.method == "POST":
        cust.name = request.form.get('name')
        cust.address = request.form.get('address')
        cust.state = request.form.get('state')
        cust.city = request.form.get('city')
        cust.phone = request.form.get('phone')
        cust.email = request.form.get('email')
        db.session.commit()
        return redirect(url_for("dashboard.customer"))
    return render_template("edit_customer.html", cust=cust)


# ------ PRODUCT ------
@edit_bp.route("/product/delete/<int:id>")
def delete_product(id):
    prod = Product.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for("dashboard.product"))

@edit_bp.route("/product/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    prod = Product.query.get_or_404(id)
    if request.method == "POST":
        prod.name = request.form.get("name")
        prod.group = request.form.get("group")
        prod.description = request.form.get('description')
        prod.price = request.form.get('price')
        db.session.commit()
        return redirect(url_for("dashboard.product"))
    return render_template("edit_product.html", prod=prod)


# ------ WAREHOUSE ------
@edit_bp.route("/warehouse/delete/<int:id>")
def delete_warehouse(id):
    wareh = Warehouse.query.get_or_404(id)
    db.session.delete(wareh)
    db.session.commit()
    return redirect(url_for("dashboard.warehouse"))

@edit_bp.route("/warehouse/edit/<int:id>", methods=["GET", "POST"])
def edit_warehouse(id):
    wareh = Warehouse.query.get_or_404(id)
    if request.method == "POST":
        wareh.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for("dashboard.warehouse"))
    return render_template("edit_warehouse.html", wareh=wareh)


# ------ WAREHOUSELOCATION ------
@edit_bp.route("/warehouseLocation/delete/<int:id>")
def delete_warehouseLocation(id):
    wareh_lo = WarehouseLocation.query.get_or_404(id)
    db.session.delete(wareh_lo)
    db.session.commit()
    return redirect(url_for("dashboard.warehouseLocation"))


@edit_bp.route("/warehouseLocation/edit/<int:id>", methods=["GET", "POST"])
def edit_warehouseLocation(id):
    wareh_lo = WarehouseLocation.query.get_or_404(id)
    if request.method == "POST":
        wareh_lo.location = request.form.get('location')
        db.session.commit()
        return redirect(url_for("dashboard.warehouseLocation"))
    return render_template("edit_warehouseLocation.html", wareh_lo=wareh_lo)


# ------ STOCK LEDGER ------
@edit_bp.route("/stockLedger/delete/<int:id>")
def delete_stockLedger(id):
    entry = StockLedger.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for("dashboard.stock_ledger"))   # ✅ fixed


# ------ PRICE GROUP ------
@edit_bp.route("/priceGroup/delete/<int:id>")
def delete_priceGroup(id):
    pg = PriceGroup.query.get_or_404(id)
    db.session.delete(pg)
    db.session.commit()
    return redirect(url_for("dashboard.price_group"))    # ✅ fixed

@edit_bp.route("/priceGroup/edit/<int:id>", methods=["GET", "POST"])
def edit_priceGroup(id):
    pg = PriceGroup.query.get_or_404(id)
    if request.method == 'POST':
        pg.name = request.form.get('name')
        db.session.commit()
        return redirect(url_for("dashboard.price_group"))  # ✅ fixed
    return render_template("edit_priceGroup.html", pg=pg)


# ------ SALES ORDER ------
@edit_bp.route("/salesOrder/delete/<int:order_id>")
def delete_sales_order(order_id):
    order = SalesOrder.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f"Sales Order #{order.id} deleted successfully!", "info")
    return redirect(url_for("dashboard.sales_orders"))    # ✅ fixed