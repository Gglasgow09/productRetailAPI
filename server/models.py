from app import db


#User Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName =  db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(35), unique=True, nullable=False)
    state = db.Column(db.String(15))
    zipcode = db.Column(db.Integer)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)
    payment = db.Column(db.String(35))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    
    def __repr__(self):
        return f"User('{self.firstName}', '{self.lastName}', {self.email}')"
    # relationships

# Review Model 
class Review(db.Model):
   __tablename__ = "reviews"
   id = db.Column(db.Integer, primary_key=True)
   rating =  db.Column (db.Integer, unique=True)

   created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
   updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    #relationships
   

# Product Model
class Product(db.Model):
    __tablename__ = "product_inventory"
    id = db.Column(db.Integer, primary_key=True)
    main_category = db.Column(db.String(30))
    title = db.Column(db.String)
    avg_rating = db.Column(db.Integer)
    features = db.Column(db.Text)
    description = db.Column(db.Text)
    store = db.Column(db.String(30))
    price = db.Column(db.Float)
    images = db.Column(db.String(100))
    videos = db.Column (db.String(100))
    categories = db.Column(db.String(100))
    details = db.Column(db.Text)
    parent_asin = db.Column(db.String(20))
    bought_together = db.Column(db.String(20))
    quantity = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    # relationships 


# Transaction Model
class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer)
    price =  db.Column(db.Integer)
    date = db.Column(db.Date, nullable=False)
    payment = db.Column(db.String(25))

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    # relationships 


    # one to many relationship between product inventory and reviews
    # one to many relationship between users and transactions 
    # many to many relationship between transactions and product inventory 