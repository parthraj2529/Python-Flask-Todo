from db import db

class UserModel(db.Model):
    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True)  # Ensure this is an integer
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

