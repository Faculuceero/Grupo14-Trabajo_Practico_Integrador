from datetime import UTC, datetime

from plataforma_qa.extensions import db


class Respuesta(db.Model):
    """Respuesta a una pregunta. La escribe un usuario o el agente de IA.

    - Respuesta de usuario: es_ia=False y user_id con el autor.
    - Respuesta del agente IA: es_ia=True, user_id vacío y agente_nombre con
      el nombre que se muestra (por ejemplo "Asistente IA").
    """

    __tablename__ = "respuestas"

    id = db.Column(db.Integer, primary_key=True)
    cuerpo = db.Column(db.Text, nullable=False)
    fecha_publicacion = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    es_aceptada = db.Column(db.Boolean, nullable=False, default=False)
    es_ia = db.Column(db.Boolean, nullable=False, default=False)
    agente_nombre = db.Column(db.String(80), nullable=True)

    pregunta_id = db.Column(
        db.Integer, db.ForeignKey("preguntas.id"), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    # Al borrar una pregunta se borran sus respuestas (si no, quedarían huérfanas).
    pregunta = db.relationship(
        "Pregunta",
        backref=db.backref("respuestas", cascade="all, delete-orphan", lazy=True),
    )
    autor = db.relationship("User", backref=db.backref("respuestas", lazy=True))

    @property
    def nombre_autor(self) -> str:
        if self.es_ia:
            return self.agente_nombre or "Agente IA"
        return self.autor.name if self.autor else "Usuario eliminado"

    def __repr__(self) -> str:
        return f"<Respuesta {self.id} de pregunta {self.pregunta_id}>"