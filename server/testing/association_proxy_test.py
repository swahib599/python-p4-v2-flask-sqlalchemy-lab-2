from app import app, db
from models import Customer, Item, Review

class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        with app.app_context():
            # Create Customer with required name
            c = Customer(name="Test Customer")
            # Create Item with required name and price
            i = Item(name="Test Item", price=10.00)
            db.session.add_all([c, i])
            db.session.commit()

            r = Review(comment='great!', customer=c, item=i)
            db.session.add(r)
            db.session.commit()

            assert hasattr(c, 'items')
            assert i in c.items