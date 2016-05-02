from sqlalchemy import Column, Integer, String, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from app import db


class Item(db.Model):
    """Model for a wishlist item"""

    __tablename__ = "Item"
    package = "info3180"

    id = Column(Integer, primary_key=True)
    info3180_username = Column(
        String(100), ForeignKey("Profile.info3180_username"), nullable=False)
    info3180_url = Column(String(500))
    info3180_title = Column(String(100))
    info3180_description = Column(String(500))
    info3180_thumbnail = Column(String(100))

    def __init__(self, username=None, url=None, title=None, description=None, thumbnail=None):
        self.info3180_username = username
        self.info3180_url = url
        self.info3180_title = title
        self.info3180_description = description
        self.info3180_thumbnail = thumbnail
