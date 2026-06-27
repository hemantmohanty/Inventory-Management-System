from flask import Blueprint, render_template
from app.models import Customer, PriceGroup, Product, Warehouse, StockLedger, SalesOrder, WarehouseLocation

# Blueprint registered as "dashboard"
dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/customer", methods=["GET", "POST"])
def customer():
    customers = Customer.query.all()
    return render_template("customer.html", customers=customers)


@dashboard_bp.route("/product", methods=["GET", "POST"])
def product():
    products = Product.query.all()
    return render_template("product.html", products=products)


@dashboard_bp.route("/warehouse", methods=["GET", "POST"])
def warehouse():
    warehouses = Warehouse.query.all()
    return render_template("warehouse.html", warehouses=warehouses)

@dashboard_bp.route("/warehouseLocation", methods=["GET", "POST"])
def warehouseLocation():
    warehouseLocations = WarehouseLocation.query.all()
    return render_template("warehouseLocation.html", warehouseLocations=warehouseLocations)

    

@dashboard_bp.route("/stockLedger", methods=["GET", "POST"])
def stock_ledger():
    ledgers = StockLedger.query.all()
    return render_template("stock-ledger.html", ledgers=ledgers)


@dashboard_bp.route("/priceGroup", methods=["GET", "POST"])
def price_group():
    pricegroups = PriceGroup.query.all()
    return render_template("price-group.html", pricegroups=pricegroups)



# List all sales orders
@dashboard_bp.route("/salesOrders")
def sales_orders():
    orders = SalesOrder.query.order_by(SalesOrder.date.desc()).all()
    return render_template("sales_orders.html", orders=orders)

# View sales order details
@dashboard_bp.route("/salesOrder/<int:order_id>")
def sales_order_detail(order_id):
    order = SalesOrder.query.get_or_404(order_id)
    return render_template("sales_order_detail.html", order=order)

