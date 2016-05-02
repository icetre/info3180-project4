from flask.ext.wtf import Form
from wtforms import StringField, validators, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):

    info3180_username = StringField(
        "username", [DataRequired("username cannot be empty")])
    info3180_password = PasswordField(
        "password", [DataRequired("password cannot be empty")])
