from flask.ext.wtf import Form
from wtforms import StringField, validators, PasswordField
from wtforms.validators import DataRequired, URL


class UrlForm(Form):
    info3180_url = StringField(
        "url", [DataRequired("Must have url"), URL(False, "Please enter a valid url")])
