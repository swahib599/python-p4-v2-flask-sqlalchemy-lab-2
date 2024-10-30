# testing/conftest.py
import pytest
from app import app, db
from models import Customer, Item, Review

@pytest.fixture(autouse=True)
def app_context():
    """Create tables before each test and clean up after"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['TESTING'] = True
    
    with app.app_context():
        # Create all tables
        db.create_all()
        yield
        # Clean up
        db.session.remove()
        db.drop_all()

def pytest_itemcollected(item):
    """Format test names in output"""
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))