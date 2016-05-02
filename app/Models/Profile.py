from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from app import db


class Profile(db.Model):
    """Model for a User profile"""
    __tablename__ = 'Profile'

    id = Column(Integer, primary_key=True)
    item = relationship('Item', lazy='joined')
    info3180_password = Column(String(100))
    info3180_email = Column(String(100))
    info3180_username = Column(
        String(100), nullable=False, index=True)

    def __init__(self, username=None, password=None, email=None):
        self.info3180_username = username
        self.info3180_password = password
        self.info3180_email = email

    def validate(self):
        user = Profile.query.filter_by(
            info3180_username=self.info3180_username).first()
        if user == None:
            return False
        if user.info3180_password == self.info3180_password:
            return True
        else:
            return False
