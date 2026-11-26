"""Votos +1 / -1 sobre preguntas y respuestas.

Regla: un usuario tiene como máximo un voto por publicación.
    - Votar por primera vez: se crea el voto.
    - Votar lo contrario:    el voto se cambia (de +1 a -1 o al revés).
    - Votar lo mismo otra vez: el voto se retira.
"""

from plataforma_qa.extensions import db
from plataforma_qa.models import Pregunta, Voto
from plataforma_qa.publicaciones.tipo_voto import TipoVoto


def valor_a_tipo(valor) -> TipoVoto:
    if isinstance(valor, bool) or valor not in (1, -1):
        raise ValueError("El voto debe ser 1 o -1.")
    return TipoVoto.POSITIVO if valor == 1 else TipoVoto.NEGATIVO


def puntuacion(publicacion) -> int:
    """Votos positivos menos votos negativos (0 si no hay votos)."""
    return sum(1 if v.tipo == TipoVoto.POSITIVO else -1 for v in publicacion.votos)


def votar(publicacion, usuario, valor) -> int:
    """Registra el voto y devuelve la puntuación resultante de la publicación."""
    if usuario is None:
        raise PermissionError("Tenés que iniciar sesión para votar.")
    tipo = valor_a_tipo(valor)

    if isinstance(publicacion, Pregunta):
        campo, filtro = "pregunta_id", Voto.pregunta_id
    else:
        campo, filtro = "respuesta_id", Voto.respuesta_id

    existente = db.session.scalar(
        db.select(Voto).where(Voto.user_id == usuario.id, filtro == publicacion.id)
    )
    if existente is None:
        db.session.add(Voto(user_id=usuario.id, tipo=tipo, **{campo: publicacion.id}))
    elif existente.tipo == tipo:
        db.session.delete(existente)
    else:
        existente.tipo = tipo
    db.session.commit()
    return puntuacion(publicacion)