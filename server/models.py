from app import db

#User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Review Model 
class Review(db.Model):
   pass


# Product Model
class Product(db.Model):
    pass



# Transaction Model
class Transaction(db.Model):
    pass

    