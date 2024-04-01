# class Config:
#     SECRET_KEY = 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://username:password@host:port/clothing_data'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# if we want to connect to AWS
    # the host will be listed on amazon account
# dialect+driver://username:password@host:port/database


# # models.py
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String

# Base = declarative_base()

# class Item(Base):
#     __tablename__ = 'items'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255))
#     description = Column(String(255))

# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import Base  # Import the Base from models.py

# DATABASE_URI = 'mysql+pymysql://username:password@localhost/your_database_name'

# engine = create_engine(DATABASE_URI)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def init_db():
#     Base.metadata.create_all(bind=engine)

# from flask import Flask, render_template
# from database import SessionLocal  # Import the session factory
# from models import Item

# app = Flask(__name__)

# @app.route('/')
# def show_items():
#     # Create a session
#     db = SessionLocal()
#     try:
#         items = db.query(Item).all()
#         return render_template('items.html', items=items)
#     finally:
#         db.close()  # Make sure to close the session

# if __name__ == '__main__':
#     app.run(debug=True)


# use pandas to read and push to the db