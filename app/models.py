from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    address = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(200), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    group = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float, default=0.0)


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class WarehouseLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(200))


class StockLedger(db.Model):
    __tablename__ = "stock_ledger"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    warehouse_location_id = db.Column(db.Integer, db.ForeignKey('warehouse_location.id'), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship("Product", backref="ledger_entries")
    warehouse = db.relationship("Warehouse", backref="ledger_entries")
    warehouse_location = db.relationship("WarehouseLocation", backref="ledger_entries")


class PriceGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))


class SalesOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="Pending")
    total_amount = db.Column(db.Float, default=0.0)
    remarks = db.Column(db.String(200))

    customer = db.relationship("Customer", backref="sales_orders")

    # ✅ Relationship corrected — ensures order.items works perfectly
    items = db.relationship(
        "SalesOrderItem",
        back_populates="sales_order",
        cascade="all, delete-orphan"
    )


class SalesOrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)

    # ✅ Proper relationship back to SalesOrder
    sales_order = db.relationship("SalesOrder", back_populates="items")
    product = db.relationship("Product", backref="order_items")
