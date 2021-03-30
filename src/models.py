from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    td_task = db.Column(db.String(120), unique=False, nullable=False)
    is_done = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Todolist %r>' % self.td_task

    def serialize(self):
        return {
            "id": self.id,
            "label": self.td_task,
            "done": self.is_done
        }




class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }