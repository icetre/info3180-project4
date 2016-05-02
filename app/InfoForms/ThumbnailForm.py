from flask.ext.wtf import Form
from wtforms import StringField, validators, PasswordField
from wtforms.validators import DataRequired, URL
from UrlForm import UrlForm


class ThumbnailForm(UrlForm):
    info3180_title = StringField(
        "title", [DataRequired("Cannot have empty title")])
    info3180_description = StringField("description", [DataRequired(
        "Cannot have empty description")])
