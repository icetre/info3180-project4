from flask.ext.wtf import Form
from LoginForm import LoginForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from ..Models.Profile import Profile
from ..Validators.DuplicateUser import DuplicateUser


class RegisterForm(Form):
    info3180_username = StringField("info3180_username", [DataRequired(
        "username cannot be empty"), DuplicateUser("A user with this username already exists")])
    info3180_password = PasswordField(
        "info3180_password", [DataRequired("password cannot be empty")])
    info3180_retype_password = PasswordField(
        "info3180_retype_password", [EqualTo('info3180_password', "Both passwords mmust be the same")])
    info3180_email = StringField("info3180_email", [DataRequired(
        "Email cannot be empty"), Email("Provide a valid email address")])
