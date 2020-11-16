from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

app =  Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
path = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "JaiMataDi"
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
patch_request_class(app)

db = SQLAlchemy(app)
Migrate(app, db)
manager_login = LoginManager()
manager_login.init_app(app)
manager_login.login_view = "customers.customerlogin"
manager_login.login_message = u'Please login first'

from shop.admin.routes import admin
from shop.core.routes import core
from shop.products.routes import products
from shop.carts.routes import carts
from shop.customers.routes import customers


app.register_blueprint(admin)
app.register_blueprint(core)
app.register_blueprint(products)
app.register_blueprint(carts)
app.register_blueprint(customers)




