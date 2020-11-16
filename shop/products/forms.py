from wtforms import StringField, SubmitField, IntegerField, TextAreaField, validators, DecimalField
from wtforms.validators import DataRequired, Email, ValidationError
from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm


class AddProductForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', [validators.DataRequired()])
    stock = IntegerField('Stock', [validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])
