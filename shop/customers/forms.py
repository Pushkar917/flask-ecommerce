from flask import request
from flask_wtf import FlaskForm
from shop.models import CustomerDB
from wtforms.validators import DataRequired, Email, ValidationError


class RegistrationForm(FlaskForm):
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    country = request.form.get('country')
    state = request.form.get('state')
    city = request.form.get('city')
    contact = request.form.get('contact')
    address = request.form.get('address')
    zipcode = request.form.get('zipcode')

    def check_email(self, email):
        if CustomerDB.query.filter_by(email=email).first():
            return True
        else:
            return False

    def check_username(self, username):
        if CustomerDB.query.filter_by(username=username).first():
            return True
        else:
            return False


class LoginForm(FlaskForm):
    email = request.form.get('email')
    password = request.form.get('password')
