from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

from shop import db, manager_login


@manager_login.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))
    username = db.Column(db.String(256), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return "{} User".format(self.username)

    def checkPassword(self, password):
        boolPasswordCheck = check_password_hash(self.password_hash, password)
        return boolPasswordCheck


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow)
    brand = db.relationship('Brands', backref=db.backref('brands', lazy=True))
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    category = db.relationship('Category', backref=db.backref('category', lazy=True))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    image_1 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_2 = db.Column(db.String(150), nullable=False, default='image.jpg')
    image_3 = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Addproduct %r' % self.name


class Brands(db.Model):
    __tablename__ = "brands"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)

    def __init__(self, name):
        self.name = name


class CustomerDB(db.Model, UserMixin):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), unique=True, index=True)
    email = db.Column(db.String(256), nullable=False)
    password_hash = db.Column(db.String(128))
    country = db.Column(db.Text, nullable=False)
    state = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text, nullable=False)
    contact = db.Column(db.Text, nullable=False)
    address = db.Column(db.Text, nullable=False)
    zipcode = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __init__(self, email, username, password, country, zipcode, state, city, contact, address, image):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.zipcode = zipcode
        self.country = country
        self.state = state
        self.city = city
        self.contact = contact
        self.address = address
        self.image = image

    def __repr__(self):
        return "{} User".format(self.username)

    def checkPasswordforCustomer(self, password):
        boolPasswordCheck = check_password_hash(self.password_hash, password)
        return boolPasswordCheck


class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class CustomerOrder(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, index=True)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    orders = db.Column(JsonEncodedDict)

    def __repr__(self):
        return '<CustomerOrder %r>' % self.invoice
