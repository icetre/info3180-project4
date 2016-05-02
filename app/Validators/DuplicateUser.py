from ..Models.Profile import Profile
from wtforms.validators import ValidationError


class DuplicateUser(object):
    """Verifies if a user 
    with the same username has already registered
    """

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        username = field.data
        if Profile.query.filter_by(info3180_username=username).first():
            raise ValidationError(self.message)
