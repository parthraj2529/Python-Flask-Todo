from db import db

class TaskModel(db.Model):
    __tablename__ = "tasks"


    id = db.Column(db.Integer, primary_key=True)  # Ensure this is an integer
    name = db.Column(db.String(128), nullable=False)
