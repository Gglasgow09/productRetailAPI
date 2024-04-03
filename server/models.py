from config import db
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    first_name =  db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(35), unique=True, nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zip = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    payment = db.Column(db.String(35), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())
    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', {self.email}')"
    # relationships
    transactions = relationship("Transaction", backref="user")
    reviews = relationship("Review", backref="user")

# Review Model 
class Review(db.Model, SerializerMixin):
   __tablename__ = "reviews"
   id = db.Column(db.Integer, primary_key=True)
   rating =  db.Column (db.Integer, unique=True, nullable=False)
   created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
   updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    #relationships
   user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
   product_id = db.Column(db.Integer, db.ForeignKey("product_inventory.id"))

   

# Product Model
class Product(db.Model, SerializerMixin):
    __tablename__ = "product_inventory"
    id = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String(30),nullable=False)
    title = db.Column(db.String,nullable=False)
    avg_rating = db.Column(db.Integer,nullable=False)
    features = db.Column(db.Text,nullable=False)
    store = db.Column(db.String(30),nullable=False)
    price = db.Column(db.Float,nullable=False)
    categories = db.Column(db.String(100),nullable=False)
    parent_asin = db.Column(db.String(20),nullable=False)
    bought_together = db.Column(db.String(20),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    # relationships 
    reviews = relationship("Review", backref="product")
    transactions = relationship("Transaction", secondary="transaction_product_association", 
                                backref="associated_products")


# Transaction Model
class Transaction(db.Model, SerializerMixin):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price =  db.Column(db.Integer,nullable=False)
    date = db.Column(db.Date, nullable=False)
    payment = db.Column(db.String(25),nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    # relationships 
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    products = relationship("Product", secondary="transaction_product_association", 
                            backref="associated_transactions")

# Association table for the many-to-many relationship between Transaction and Product
transaction_product_association = db.Table('transaction_product_association',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transactions.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product_inventory.id'))
)