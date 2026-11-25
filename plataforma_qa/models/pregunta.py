from datetime import UTC, datetime

from plataforma_qa.extensions import db

pregunta_etiqueta = db.Table(
    "pregunta_etiqueta",
    db.Column(
        "pregunta_id",
        db.Integer,
        db.ForeignKey("preguntas.id"),
        primary_key=True,
    ),
    db.Column(
        "etiqueta_id",
        db.Integer,
        db.ForeignKey("etiquetas.id"),
        primary_key=True,
    ),
)


class Pregunta(db.Model):
    __tablename__ = "preguntas"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    categoria_id = db.Column(
        db.Integer, db.ForeignKey("categorias.id"), nullable=False
    )

    autor = db.relationship("User", backref=db.backref("preguntas", lazy=True))
    categoria = db.relationship("Categoria", back_populates="preguntas")
    etiquetas = db.relationship(
        "Etiqueta",
        secondary=pregunta_etiqueta,
        backref=db.backref("preguntas", lazy=True),
    )

    def __repr__(self) -> str:
        return f"<Pregunta {self.id}: {self.titulo}>"