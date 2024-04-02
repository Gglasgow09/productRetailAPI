from flask import render_template, url_for, redirect, flash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from config import app, db, bcrypt


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstName =  db.Column(db.String(25), nullable=False)
    lastName = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(35), unique=True, nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
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
    description = db.Column(db.Text,nullable=False)
    store = db.Column(db.String(30),nullable=False)
    price = db.Column(db.Float,nullable=False)
    images = db.Column(db.String(100),nullable=False)
    videos = db.Column (db.String(100),nullable=False)
    categories = db.Column(db.String(100),nullable=False)
    details = db.Column(db.Text,nullable=False)
    parent_asin = db.Column(db.String(20),nullable=False)
    bought_together = db.Column(db.String(20),nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    # relationships 
    reviews = relationship("Review", backref="product")
    transactions = relationship("Transaction", secondary="transaction_product_association", backref="associated_products")


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
    products = relationship("Product", secondary="transaction_product_association", backref="associated_transactions")

# Association table for the many-to-many relationship between Transaction and Product
transaction_product_association = db.Table('transaction_product_association',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transactions.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product_inventory.id'))
)

db.init_app(app)

with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("ERROR! Username is taken!")
        
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Sucess!!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong Password")
            
    return render_template('login.html', form=form)

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard',  methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')
        

if __name__ == "__main__":
    app.run()