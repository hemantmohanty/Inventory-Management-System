from flask import Blueprint, render_template, redirect, request, url_for, flash
from datetime import date
from app import db
from app.models import Customer, PriceGroup, Product, Warehouse, WarehouseLocation, StockLedger, SalesOrderItem, SalesOrder

create_bp = Blueprint("create", __name__)


# 🧾 ADD CUSTOMER
@create_bp.route("/customer/add", methods=["POST", "GET"])
def add_customer():
    if request.method == "POST":
        name = request.form.get('name')
        address = request.form.get('address')
        state = request.form.get('state')
        city = request.form.get('city')
        phone = request.form.get('phone')
        email = request.form.get('email')

        # ⚙️ CHANGE: Added duplicate check + phone validation
        if Customer.query.filter_by(name=name).first():
            flash("Customer name already exists.", "danger")
            return redirect(url_for("create.add_customer"))
        if len(phone) < 10:
            flash("Number must be at least 10 digits.", "danger")
            return redirect(url_for("create.add_customer"))

        new_customer = Customer(
            name=name, address=address, state=state,
            city=city, phone=phone, email=email
        )
        db.session.add(new_customer)
        db.session.commit()
        flash("Customer added successfully!", "success")  # ⚙️ CHANGE: Added flash
        return redirect(url_for("dashboard.customer"))

    return render_template("add_customer.html")


# 📦 ADD PRODUCT
@create_bp.route("/product/add", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        name = request.form.get('name')
        group = request.form.get('group')
        description = request.form.get('description')
        price = request.form.get('price')

        # ⚙️ CHANGE: Convert price safely to float
        try:
            price = float(price)
        except (ValueError, TypeError):
            flash("Invalid price format!", "danger")
            return redirect(url_for("create.add_product"))

        new_product = Product(
            name=name, group=group, description=description, price=price
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully!", "success")
        return redirect(url_for("dashboard.product"))

    return render_template("add_product.html")


# 🏢 ADD WAREHOUSE
@create_bp.route("/warehouse/add", methods=["GET", "POST"])
def add_warehouse():
    if request.method == "POST":
        name = request.form.get('name')
        if not name:
            flash("Warehouse name is required.", "danger")
            return redirect(url_for("create.add_warehouse"))

        new_warehouse = Warehouse(name=name)
        db.session.add(new_warehouse)
        db.session.commit()
        flash("Warehouse added successfully!", "success")
        return redirect(url_for("dashboard.warehouse"))

    return render_template('add_warehouse.html')


# 📍 ADD WAREHOUSE LOCATION
@create_bp.route("/warehouseLocation/add", methods=["GET", "POST"])
def add_warehouseLocation():
    if request.method == "POST":
        location = request.form.get('location')
        if not location:
            flash("Location is required.", "danger")
            return redirect(url_for("create.add_warehouseLocation"))

        new_warehouse = WarehouseLocation(location=location)
        db.session.add(new_warehouse)
        db.session.commit()
        flash("Warehouse location added successfully!", "success")
        return redirect(url_for("dashboard.warehouseLocation"))

    return render_template('add_warehouseLocation.html')


# 📘 ADD STOCK LEDGER ENTRY
@create_bp.route("/stockLedger/add", methods=["GET", "POST"])
def add_stockLedger():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        warehouse_id = request.form.get("warehouse_id")
        warehouse_location_id = request.form.get("warehouse_location_id")
        quantity = request.form.get("quantity")

        # ⚙️ CHANGE: Ensure valid quantity
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            flash("Quantity must be a number!", "danger")
            return redirect(url_for("create.add_stockLedger"))

        entry = StockLedger(
            product_id=product_id,
            warehouse_id=warehouse_id,
            warehouse_location_id=warehouse_location_id,
            quantity=quantity
        )
        db.session.add(entry)
        db.session.commit()
        flash("Stock entry added successfully!", "success")
        return redirect(url_for("dashboard.stock_ledger"))

    products = Product.query.all()
    warehouses = Warehouse.query.all()
    warehouseLocations = WarehouseLocation.query.all()
    return render_template("add_stockLedger.html", products=products, warehouses=warehouses, warehouseLocations=warehouseLocations)


# 💰 ADD PRICE GROUP
@create_bp.route("/priceGroup/add", methods=["GET", "POST"])
def add_priceGroup():
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            flash("Price group name is required.", "danger")
            return redirect(url_for("create.add_priceGroup"))

        new_priceGroup = PriceGroup(name=name)
        db.session.add(new_priceGroup)
        db.session.commit()
        flash("Price group added successfully!", "success")
        return redirect(url_for("dashboard.price_group"))

    return render_template("add_priceGroup.html")


@create_bp.route("/salesOrder/new", methods=["GET", "POST"])
def viws_sales_order():
    customers = Customer.query.all()
    products = Product.query.all()

    if request.method == "POST":
        customer_id = request.form.get("customer_id")
        remarks = request.form.get("remarks", "")

        if not customer_id:
            flash("Customer is required!", "danger")
            return redirect(url_for("create.viws_sales_order"))

        # Create order
        order = SalesOrder(
            customer_id=customer_id,
            date=date.today(),
            remarks=remarks,
            status="Pending",
            total_amount=0
        )
        db.session.add(order)
        db.session.commit()

        # Single product logic
        product_id = request.form.get("product_id")
        qty = request.form.get("quantity", "0")
        try:
            qty = int(qty)
        except ValueError:
            qty = 0

        if qty > 0 and product_id:
            product = Product.query.get(product_id)
            if product:
                item_total = float(product.price) * qty
                order.total_amount = item_total

                item = SalesOrderItem(
                    sales_order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    unit_price=float(product.price),
                    total=item_total
                )
                db.session.add(item)
                db.session.commit()  # commit items + total_amount

        flash("Sales Order created successfully!", "success")
        return redirect(url_for("dashboard.sales_orders"))

    # ✅ IMPORTANT: GET request must return render_template
    return render_template("new_sales_order.html", customers=customers, products=products)
