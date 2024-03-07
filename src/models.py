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
    files = db.relationship("Files", back_populates="user")
    message = db.relationship("Message", back_populates="user")

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
        }

class Admins(db.Model): #Parent
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=False, nullable=False)
    hashed_password = db.Column(db.String(150), unique=False, nullable=False)
    salt = db.Column(db.String(150), unique=False, nullable=False)
    message = db.relationship("Message", back_populates="admins")


    def __repr__(self):
        return '<Admin %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username
        }

class Receipt(db.Model): #Child
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(150), unique=False, nullable=False)
    file = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="receipt") 

    def __repr__(self):
        return '<Receipt %r>' % self.number

    def serialize(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "file": self.file,
            "user_id": self.user_id,
        }

class Files(db.Model): #Child
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    file = db.Column(db.String(500), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="receipt") 

    def __repr__(self):
        return '<Files %r>' % self.number

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
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

class Message(db.Model):  #Child 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    admins_id = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    sender = db.Column(db.String(100), unique=False, nullable=False)
    user = db.relationship("User", back_populates="message") 
    admins = db.relationship("Admins", back_populates="message") 


    def __repr__(self):
        return '<Message %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "message": self.message,
            "user_id": self.user_id,
            "admin_id": self.admin_id,
            "sender": self.sender
        }

