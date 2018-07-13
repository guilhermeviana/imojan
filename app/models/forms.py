from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, FloatField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    passwords = PasswordField("passwords", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class Home(Form):
    title = StringField("title", validators=[DataRequired()])
    value = StringField("value", validators=[DataRequired()])
    description = TextAreaField("description")
    zipCode = StringField("zipCode", validators=[DataRequired()])
    street = StringField("zipCode", validators=[DataRequired()])
    number = IntegerField("number", validators=[DataRequired()])
    neighborhood = StringField("neighborhood", validators=[DataRequired()])
    complement = StringField("complement")
    telephone = StringField("telephone")
