from flask import Flask, render_template, url_for, redirect, flash, session, request
from flask import session as login_session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, EmailField, validators, HiddenField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amazon.db'
app.config['SECRET_KEY'] = 'password'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#---------CLASSES (MODELS and FORMS)--------------------------------------------------------------------------------------------

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
    # cart_items = db.relationship('Cart', backref='Inventory', lazy=True)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    # product_id = db.Column(db.Integer, db.ForeignKey('Inventory.index'), nullable=False)
    username = db.Column(db.String)
    product_name = db.Column(db.String)
    # quantity = db.Column(db.Integer, default=1)
    # product = db.relationship('Inventory')
    # Additional fields like user_id can be added for user-specific carts
    # def add_to_cart(self, product_id):
    #     pass
    #     # Logic to add a product to the cart

    # def delete_item(self):
    #     db.session.delete(self)
    #     db.session.commit()

    # def update_quantity(self, new_quantity):
    #     if new_quantity > 0:
    #         self.quantity = new_quantity
    #     else:
    #         db.session.delete(self)
    #     db.session.commit()


class Review(db.Model, UserMixin):
   __tablename__ = "Review"
   id = db.Column(db.Integer, primary_key=True)
   product_name = db.Column(db.String)
#    rating =  db.Column (db.Integer, unique=True, nullable=False)
   username = db.Column(db.String(30))
   review = db.Column(db.String)
#    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
#    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
#                           onupdate=db.func.current_timestamp())
    
   

with app.app_context():
    db.create_all()

#create Registration Form
class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    first_name = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "First Name"})
    last_name = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})
    email = EmailField(validators=[InputRequired(), validators.Email()], render_kw={"placeholder": "EMAIL"})
    phone = StringField(validators=[InputRequired()], render_kw={"placeholder": "Phone-must be 10 digits"})
    state = SelectField('STATE', choices=[('NY', 'New York'), ('CO', 'Colorado'), ('VA', 'Virginia')])
    zip_code = StringField(validators=[InputRequired()], render_kw={"placeholder": "Zip-must be 5 digits"})
    payment = SelectField('Payment', choices=[('cr', 'Credit'), ('ck', 'Check'), ('la', 'Layaway')])
    submit = SubmitField("Register")

    #validate username
    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()
        if existing_username:
            raise ValidationError("ERROR! Username is taken!")
        
#create login form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    gender = SelectField('Style', validators=[InputRequired()], choices=[('ALL', 'ALL'), ('Men', 'Mens'), ('Women', 'Womens'), ('Boys', 'Boys'), ('Girls', 'Girls')])
    type = SelectField('Type', choices=[('ALL', 'ALL'), ('Clothing', 'Clothing'), ('Shoes', 'Shoes'), ('Accessories', 'Accessories'), ('Jewelry', 'Jewelry')])
    sort = SelectField('Sort', choices=[('ANY', 'ANY'), ('price', 'Price'), ('average_rating', 'Rating')])
    submit = SubmitField("Search")

class WriteReview(FlaskForm):
    username = HiddenField()
    review = TextAreaField(validators=[InputRequired()])
    submit = SubmitField("Submit")

class AddCart(FlaskForm):
    username = HiddenField()
    product_name = HiddenField()
    submit = SubmitField("Add to Cart")

##--------------ROUTES---------------------------------------------------------------------------------------------------------------

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
                session['username'] = form.username.data
                return redirect(url_for('dashboard'))
            else:
                flash("Attention!!! Password Incorrect!!!")
        else:
            flash("Attention!!! User Not Found!!!")     
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
        new_user = User(username=form.username.data, password=hashed_pass,
                        first_name=form.first_name.data, last_name=form.last_name.data,
                        email=form.email.data, phone=form.phone.data, state=form.state.data, 
                        zip_code=form.zip_code.data, payment=form.payment.data)
        name=form.first_name.data
        db.session.add(new_user)
        db.session.commit()
        flash("User Sucessfully Created!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/browse', methods=['GET', 'POST'])
@login_required
def browse():

    form = SearchForm()

    if form.gender.data == 'ALL' and form.type.data == 'ALL':
        if form.sort.data == 'ANY':
            items = Inventory.query.filter_by()
            return render_template('browse.html', items=items, form=form)
        elif form.sort.data == 'average_rating':
            items = Inventory.query.order_by(Inventory.average_rating.desc())
            return render_template('browse.html', items=items, form=form)
        else: 
            items = Inventory.query.order_by(Inventory.price)
            return render_template('browse.html', items=items, form=form)

    elif form.gender.data != 'ALL' and form.type.data == 'ALL':
        if form.sort.data == 'ANY':
            items = Inventory.query.filter_by(gender=form.gender.data)
            return render_template('browse.html', items=items, form=form)
        elif form.sort.data == 'average_rating':
            items = Inventory.query.filter_by(gender=form.gender.data).order_by(Inventory.average_rating.desc())
            return render_template('browse.html', items=items, form=form)
        else: 
            items = Inventory.query.filter_by(gender=form.gender.data).order_by(Inventory.price)
            return render_template('browse.html', items=items, form=form)
        
    elif form.gender.data != 'ALL' and form.type.data != 'ALL':
        if form.sort.data == 'ANY':
            items = Inventory.query.filter_by(gender=form.gender.data, type=form.type.data)
            return render_template('browse.html', items=items, form=form)
        elif form.sort.data == 'average_rating':
            items = Inventory.query.filter_by(gender=form.gender.data, type=form.type.data).order_by(Inventory.average_rating.desc())
            return render_template('browse.html', items=items, form=form)
        else: 
            items = Inventory.query.filter_by(gender=form.gender.data, type=form.type.data).order_by(Inventory.price)
            return render_template('browse.html', items=items, form=form)
        
    else: 
        if form.sort.data == 'ANY':
            items = items = Inventory.query.filter_by(type=form.type.data)
            return render_template('browse.html', items=items, form=form)
        elif form.sort.data == 'average_rating':
            items = items = Inventory.query.filter_by(type=form.type.data).order_by(Inventory.average_rating.desc())
            return render_template('browse.html', items=items, form=form)
        else: 
            items = items = Inventory.query.filter_by(type=form.type.data).order_by(Inventory.price)
            return render_template('browse.html', items=items, form=form)
         

@app.route('/reviews', methods=['GET', 'POST'])
@login_required
def reviews():
    items = Review.query.all()
    return render_template('reviews.html', items=items)
    

@app.route('/new_review/<string:product_name>', methods=['GET', 'POST'])
@login_required
def new_review(product_name):
    form = WriteReview()
    p_name = product_name
    if form.validate_on_submit():
        new_review = Review(product_name=p_name, username=session['username'],
                        review=form.review.data)
        db.session.add(new_review)
        db.session.commit()
        flash("Review Sucessfully Created!")
        return redirect(url_for('browse'))
    return render_template('new_review.html', form=form)

@app.route('/add/<string:product_name>', methods=['GET', 'POST'])
@login_required
def add(product_name):
    form = AddCart()
    if form.validate_on_submit():
        add_item = Cart(product_name=product_name, username=session['username'])
        db.session.add(add_item)
        db.session.commit()
        flash("Item Added to Cart!")
        return redirect(url_for('view_cart'))
    return render_template('add.html', form=form)

# @app.route('/remove/<int:product_id>', methods=['POST'])
# def remove(cart_id):
#     cart_item = Cart.query.get_or_404(cart_id)
#     cart_item.delete_item()
#     return redirect(url_for('view_cart'))

# @app.route('/update/<int:cart_id>', methods=['POST'])
# def update_cart(cart_id):
#     cart_item = Cart.query.get_or_404(cart_id)
#     new_quantity = request.form.get('quantity', type=int)
#     cart_item.update_quantity(new_quantity)
#     return redirect(url_for('view_cart'))

@app.route('/view_cart', methods=['GET', 'POST'])
@login_required
def view_cart():
    cart_items = Cart.query.all()
    return render_template('view_cart.html', cart_items=cart_items)

        
if __name__ == "__main__":
    app.run(debug=True)