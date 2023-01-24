from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Users(db.model):
    '''Users Table'''
    
    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    hashed_password = db.Column(db.String(255))
    created = db.Column(db.DateTime)
    
    # ratings = a list of Rating objects

    def __repr__(self):
        return f"<{self.username}, user_id={self.user_id}, email={self.email}, joined={self.created}>"
    
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        self.created = datetime.now()


def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = app
    db.init_app(app)
    
if __name__ == '__main__':
    app = Flask(__name__)
    connect_to_db(app)
    print('Connected to db!')