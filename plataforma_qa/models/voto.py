from datetime import UTC, datetime

from plataforma_qa.extensions import db
from plataforma_qa.publicaciones.tipo_voto import TipoVoto


class Voto(db.Model):
    """Voto +1 (POSITIVO) o -1 (NEGATIVO) de un usuario sobre una publicación.

    La publicación es una pregunta O una respuesta (nunca las dos, nunca
    ninguna) y cada usuario tiene como máximo un voto por publicación.
    """

    __tablename__ = "votos"
    __table_args__ = (
        db.UniqueConstraint("user_id", "pregunta_id", name="uq_voto_usuario_pregunta"),
        db.UniqueConstraint(
            "user_id", "respuesta_id", name="uq_voto_usuario_respuesta"
        ),
        db.CheckConstraint(
            "(pregunta_id IS NOT NULL AND respuesta_id IS NULL)"
            " OR (pregunta_id IS NULL AND respuesta_id IS NOT NULL)",
            name="ck_voto_una_publicacion",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Enum(TipoVoto, native_enum=False, length=20), nullable=False)
    fecha = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey("preguntas.id"), nullable=True)
    respuesta_id = db.Column(
        db.Integer, db.ForeignKey("respuestas.id"), nullable=True
    )

    votante = db.relationship("User", backref=db.backref("votos", lazy=True))
    # Al borrar la publicación se borran sus votos.
    pregunta = db.relationship(
        "Pregunta",
        backref=db.backref("votos", cascade="all, delete-orphan", lazy=True),
    )
    respuesta = db.relationship(
        "Respuesta",
        backref=db.backref("votos", cascade="all, delete-orphan", lazy=True),
    )

    def __repr__(self) -> str:
        return f"<Voto {self.id} {self.tipo}>"