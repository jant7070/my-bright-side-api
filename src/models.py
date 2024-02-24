from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model): #Parent
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(150), unique=False, nullable=False)
    salt = db.Column(db.String(150), unique=False, nullable=False)
    receipt = db.relationship("Receipt", back_populates="user")
    photos = db.relationship("Photos", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
        }

class Receipt(db.Model): #Child
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    file = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="receipt") 

    def __repr__(self):
        return '<Receipt %r>' % self.number

    def serialize(self):
        return {
            "id": self.id,
            "number": self.number,
            "file": self.file,
            "user_id": self.user_id,
        }


class Photos(db.Model): #Child
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="photos") 

    def __repr__(self):
        return '<Photos %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "file": self.file,
            "user_id": self.user_id,
        }

class News(db.Model):   
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String(1000), unique=False, nullable=False)

