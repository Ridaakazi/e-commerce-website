from datetime import datetime
from app import db
from flask_login import UserMixin

#  association table
user_product_association = db.Table(
    'user_product_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('added_at', db.DateTime, default=datetime.utcnow),
    db.UniqueConstraint('user_id', 'product_id', name='unique_user_product')
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    # Def many-to-many 
    products = db.relationship('Product', secondary=user_product_association, back_populates='users')
    carts = db.relationship('UserCart', back_populates='user')

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(50), nullable=False)
    in_wishlist = db.Column(db.Boolean, default=False)
    stock = db.Column(db.Integer, nullable=False)

     # Def many-to-many 
    users = db.relationship('User', secondary=user_product_association, back_populates='products')
    carts = db.relationship('UserCart', back_populates='product')

class UserCart(db.Model):
    __tablename__ = 'user_cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='carts')
    product = db.relationship('Product', back_populates='carts')

    def __repr__(self):
        return f"UserCart(id={self.id}, quantity={self.quantity}, user_id={self.user_id}, product_id={self.product_id}, added_at={self.added_at})"
