from flask.ext.wtf import Form
from wtforms.fields import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class ContactForm(Form):
    recepientAddr = StringField(
        'recepient address (comma separated)', [DataRequired("recepient address cannot be empty")])
    Subject = StringField('Subject', [DataRequired("Subject cannot be empty")])
    Body = TextAreaField('Body', [DataRequired("Body cannot be empty")])
    url = StringField('url', [DataRequired("url cannot be empty")])
