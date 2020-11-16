from shop.models import Users
from flask import request


class RegistrationForm():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    def check_email(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ("{}This email already exist :".format(field.data))

    def check_username(self, field):
        if Users.query.filter_by(email=field.data).first():
            raise ("{}This email already exist :".format(field.data))
