from flask import render_template, url_for, redirect, flash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from config import app, db, bcrypt
from models import User, Review, Product, Transaction 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/register', methods=['GET', 'POST', 'PATCH'])
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

# Route to add a product to the shopping cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    # Logic to add product to the shopping cart
    pass

# Route to process an order
@app.route('/checkout', methods=['POST'])
def checkout():
    # Logic to process the order
    pass

# Route to fetch products sorted by price
@app.route('/products/sort/price', methods=['GET'])
def sort_by_price():
    # Logic to fetch products sorted by price
    pass

# Route to fetch products sorted by popularity
@app.route('/products/sort/popularity', methods=['GET'])
def sort_by_popularity():
    # Logic to fetch products sorted by popularity
    pass

# Route to fetch products by category
@app.route('/products/category/<category_name>', methods=['GET'])
def get_products_by_category(category_name):
    # Logic to fetch products by category
    pass

# Route for custom queries and sorts
@app.route('/custom_query', methods=['GET'])
def custom_query():
    # Logic for custom queries and sorts
    pass


if __name__ == "__main__":
    app.run()