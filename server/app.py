from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from models import *
from sqlalchemy import create_engine


db = SQLAlchemy()
app = Flask(__name__)
db_name = 'clothing_data'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clothing_data'
db.init_app(app)

@app.route('/')
def index():
    
    engine = create_engine()

    db.query(Product).all()
    return product.id



if __name__ == '__main__':
    app.run(port=3306, debug=True)
