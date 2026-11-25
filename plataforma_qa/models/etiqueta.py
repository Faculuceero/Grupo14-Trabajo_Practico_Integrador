from plataforma_qa.extensions import db


class Etiqueta(db.Model):
    __tablename__ = "etiquetas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"<Etiqueta {self.nombre}>"