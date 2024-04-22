from config import db
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    first_name =  db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    state = db.Column(db.String(15))
    zip_code = db.Column(db.String(5))
    payment = db.Column(db.String(35))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

# db.init_app(app)
    
class Inventory(db.Model, UserMixin):
    __tablename__ = "Inventory"
    index = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String(190))
    title = db.Column(db.String)
    average_rating = db.Column(db.Integer)
    rating_number = db.Column(db.Integer)
    price = db.Column(db.Float)
    store = db.Column(db.String(80))
    gender = db.Column(db.Float)
    type = db.Column(db.String(100))
    misc = db.Column(db.String(130))

class Review(db.Model, UserMixin):
   __tablename__ = "reviews"
   id = db.Column(db.Integer, primary_key=True)
   product_id = db.Column(db.Integer, db.ForeignKey("Inventory.index"))
   rating =  db.Column (db.Integer, unique=True, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
   created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
   updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())