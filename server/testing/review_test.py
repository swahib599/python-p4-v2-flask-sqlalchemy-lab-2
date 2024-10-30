from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    reviews = db.relationship('Review', back_populates='customer', lazy=True)
    items = association_proxy('reviews', 'item')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [review.to_dict(include_customer=False) for review in self.reviews]
        }

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    reviews = db.relationship('Review', back_populates='item', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.to_dict(include_item=False) for review in self.reviews]
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    def to_dict(self, include_customer=True, include_item=True):
        dict_data = {
            'id': self.id,
            'comment': self.comment,
        }
        
        if include_customer:
            dict_data['customer'] = {
                'id': self.customer.id,
                'name': self.customer.name
            }
        
        if include_item:
            dict_data['item'] = {
                'id': self.item.id,
                'name': self.item.name,
                'price': self.item.price
            }
        
        return dict_data