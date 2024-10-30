from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='customer', lazy=True)
    # Association proxy to get items through reviews
    items = association_proxy('reviews', 'item')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        return name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'reviews': [{
                'id': review.id,
                'comment': review.comment,
                'item': {
                    'id': review.item.id,
                    'name': review.item.name,
                    'price': review.item.price
                }
            } for review in self.reviews]
        }

    def __repr__(self):
        return f'<Customer {self.name}>'

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='item', lazy=True)

    @validates('name', 'price')
    def validate_fields(self, key, value):
        if key == 'name' and not value:
            raise ValueError("Name cannot be empty")
        if key == 'price' and (not isinstance(value, (int, float)) or value < 0):
            raise ValueError("Price must be a positive number")
        return value

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [{
                'id': review.id,
                'comment': review.comment,
                'customer': {
                    'id': review.customer.id,
                    'name': review.customer.name
                }
            } for review in self.reviews]
        }

    def __repr__(self):
        return f'<Item {self.name} - ${self.price}>'

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    @validates('comment')
    def validate_comment(self, key, comment):
        if not comment:
            raise ValueError("Comment cannot be empty")
        return comment

    def to_dict(self):
        return {
            'id': self.id,
            'comment': self.comment,
            'customer': {
                'id': self.customer.id,
                'name': self.customer.name
            },
            'item': {
                'id': self.item.id,
                'name': self.item.name,
                'price': self.item.price
            }
        }

    def __repr__(self):
        return f'<Review {self.comment} by Customer {self.customer_id} for Item {self.item_id}>'