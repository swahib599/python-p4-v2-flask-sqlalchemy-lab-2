import pytest
from app import app, db  # Ensure this matches the correct import path
from models import Customer, Item, Review

@pytest.fixture(scope='module')
def test_client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create the database tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_review_can_be_instantiated():
    '''Test that a review can be instantiated.'''
    r = Review(comment='great product!')
    assert r
    assert isinstance(r, Review)

def test_review_has_comment():
    '''Test that review can be instantiated with a comment attribute.'''
    r = Review(comment='great product!')
    assert r.comment == 'great product!'

def test_review_can_be_saved_to_database(test_client):
    '''Test that review can be added to the database.'''
    with app.app_context():
        assert 'comment' in Review.__table__.columns
        
        # Create a Customer and Item first
