from flask import Flask
from flask_migrate import Migrate
from models import db, Customer, Item, Review  # Import models explicitly

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Create tables in app context
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return '<h1>Flask SQLAlchemy Lab 2</h1>'

if __name__ == '__main__':
    create_tables()  # Create tables when running the app directly
    app.run(port=5555, debug=True)