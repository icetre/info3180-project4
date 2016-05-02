from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config["SECRET_KEY"] = "ITSASECRET"
app.config['CSRF_ENABLED '] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://Rox116:fred116@localhost/Wishlist'
db = SQLAlchemy(app)
from app import views
