from app import db
from models import Customer, Item, Review

class TestAssociationProxy:
    '''Customer in models.py'''

    def test_has_association_proxy(self):
        '''has association proxy to items'''
        c = Customer(name='Test Customer')  # Add name
        i = Item(name='Test Item', price=10.0)  # Add required attributes
        db.session.add_all([c, i])
        db.session.commit()

        r = Review(comment='great!', customer=c, item=i)
        db.session.add(r)
        db.session.commit()

        assert hasattr(c, 'items')
        assert i in c.items

class TestSerialization:
    '''models in models.py'''

    def test_customer_is_serializable(self):
        '''customer is serializable'''
        c = Customer(name='Phil')
        i = Item(name='Test Item', price=10.0)
        db.session.add_all([c, i])
        db.session.commit()
        
        r = Review(comment='great!', customer=c, item=i)
        db.session.add(r)
        db.session.commit()
        
        customer_dict = c.to_dict()
        assert customer_dict['id']
        assert customer_dict['name'] == 'Phil'
        assert customer_dict['reviews']
        
        review = customer_dict['reviews'][0]
        assert 'comment' in review
        assert 'item' in review
        assert 'customer' not in review
        assert review['comment'] == 'great!'

    def test_item_is_serializable(self):
        '''item is serializable'''
        i = Item(name='Insulated Mug', price=9.99)
        c = Customer(name='Test Customer')
        db.session.add_all([i, c])
        db.session.commit()
        
        r = Review(comment='great!', item=i, customer=c)
        db.session.add(r)
        db.session.commit()
        
        item_dict = i.to_dict()
        assert item_dict['id']
        assert item_dict['name'] == 'Insulated Mug'
        assert item_dict['price'] == 9.99
        assert item_dict['reviews']
        
        review = item_dict['reviews'][0]
        assert 'comment' in review
        assert 'customer' in review
        assert 'item' not in review
        assert review['comment'] == 'great!'

    def test_review_is_serializable(self):
        '''review is serializable'''
        c = Customer(name='Test Customer')
        i = Item(name='Test Item', price=10.00)
        db.session.add_all([c, i])
        db.session.commit()
        
        r = Review(comment='great!', customer=c, item=i)
        db.session.add(r)
        db.session.commit()
        
        review_dict = r.to_dict()
        assert review_dict['id']
        assert review_dict['comment'] == 'great!'
        assert review_dict['customer']['name'] == 'Test Customer'
        assert review_dict['item']['name'] == 'Test Item'
        assert review_dict['item']['price'] == 10.00