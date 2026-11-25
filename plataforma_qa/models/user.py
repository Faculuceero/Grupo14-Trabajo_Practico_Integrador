from plataforma_qa.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    rol = db.Column(db.String(50), nullable=False, server_default="usuario")

    def __repr__(self):
        return f"<User {self.email} ({self.rol})>"