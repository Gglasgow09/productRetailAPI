from flask import Flask, render_template, url_for, redirect, flash
from flask_login import UserMixin,login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, EmailField, validators
from wtforms.validators import InputRequired, Length, ValidationError, DataRequired
from flask_bcrypt import bcrypt
# from config import app, db

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

# @app.context_processor
# def base():
#     form= SearchForm
#     return dict(form=form)


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

class Review(db.Model, UserMixin):
   __tablename__ = "reviews"
   id = db.Column(db.Integer, primary_key=True)
   product_id = db.Column(db.Integer, db.ForeignKey("Inventory.index"))
   rating =  db.Column (db.Integer, unique=True, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
   created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
   updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                          onupdate=db.func.current_timestamp())
    
   

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

@app.route('/register', methods=['GET', 'POST', 'PATCH'])
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
    return render_template('reviews.html')

@app.route('/new_review', methods=['GET', 'POST'])
@login_required
def new_review():
    return render_template('new_review.html')

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    items = Inventory.query.order_by(Inventory.price)
    return render_template('add.html', items=items)

        
if __name__ == "__main__":
    app.run()