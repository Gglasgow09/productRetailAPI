from flask import Flask
from models import db, User, Review, Product, Transaction
from data_import import import_json_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

@app.route('/import_data')
def import_data():
    json_file = 'Clothing_Data_Nine_Thousand_entries.json'
    table_name = 'clothing_data'
    try:
        import_json_data(json_file, table_name)
        return 'Data import successful'
    except Exception as e:
        return f'Data import failed: {str(e)}'

@app.route('/')
def index():
    # Example usage of the User model
    users = User.query.all()
    return f"Number of users: {len(users)}"

with app.app_context():
    db.create_all

if __name__ == '__main__':
    app.run(debug=True)
