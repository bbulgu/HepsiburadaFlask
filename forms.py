from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, URL, ValidationError

def hepsiburadaLinkCheck(form, field):
    print(field.data)
    print("hepsiburada.com" in field.data)
    if "hepsiburada.com" not in field.data:
        raise ValidationError('Not a hepsiburada link')

class ProductForm(FlaskForm):
    product_link = StringField('Product Link', validators=[DataRequired(), hepsiburadaLinkCheck, URL()])