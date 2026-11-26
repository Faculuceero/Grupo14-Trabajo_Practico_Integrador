"""Reglas de negocio de las respuestas.

Las rutas web (y más adelante la API y el agente de IA) llaman a estas
funciones; así las reglas viven en un solo lugar:

    ValueError      -> datos inválidos
    PermissionError -> el usuario no puede hacer eso
"""

from plataforma_qa.extensions import db
from plataforma_qa.models import Respuesta
from plataforma_qa.services.permisos import es_admin


def _limpiar(cuerpo) -> str:
    if not isinstance(cuerpo, str) or not cuerpo.strip():
        raise ValueError("La respuesta no puede estar vacía.")
    return cuerpo.strip()


def puede_modificar(respuesta, usuario) -> bool:
    """Solo el autor edita su respuesta (las del agente IA, nadie)."""
    return (
        usuario is not None
        and not respuesta.es_ia
        and respuesta.user_id == usuario.id
    )


def puede_borrar(respuesta, usuario) -> bool:
    """El autor borra la suya; el admin puede borrar cualquiera (incluso las de la IA)."""
    return es_admin(usuario) or puede_modificar(respuesta, usuario)


def puede_aceptar(pregunta, usuario) -> bool:
    """Solo el autor de la pregunta marca una respuesta como aceptada."""
    return usuario is not None and usuario.id == pregunta.user_id


def crear_respuesta(pregunta, autor, cuerpo) -> Respuesta:
    if autor is None:
        raise PermissionError("Tenés que iniciar sesión para responder.")
    respuesta = Respuesta(
        pregunta_id=pregunta.id, user_id=autor.id, cuerpo=_limpiar(cuerpo)
    )
    db.session.add(respuesta)
    db.session.commit()
    return respuesta


def crear_respuesta_ia(pregunta, cuerpo, agente_nombre="Agente IA") -> Respuesta:
    """Respuesta escrita por el agente de IA: no tiene usuario autor."""
    respuesta = Respuesta(
        pregunta_id=pregunta.id,
        user_id=None,
        es_ia=True,
        agente_nombre=agente_nombre,
        cuerpo=_limpiar(cuerpo),
    )
    db.session.add(respuesta)
    db.session.commit()
    return respuesta


def modificar_respuesta(respuesta, solicitante, cuerpo) -> Respuesta:
    if not puede_modificar(respuesta, solicitante):
        raise PermissionError("Solo el autor puede modificar su respuesta.")
    respuesta.cuerpo = _limpiar(cuerpo)
    db.session.commit()
    return respuesta


def borrar_respuesta(respuesta, solicitante) -> None:
    if not puede_borrar(respuesta, solicitante):
        raise PermissionError("Solo el autor o un administrador pueden borrar la respuesta.")
    db.session.delete(respuesta)
    db.session.commit()


def aceptar_respuesta(respuesta, solicitante) -> Respuesta:
    """Marca esta respuesta como aceptada y desmarca las demás de la pregunta."""
    pregunta = respuesta.pregunta
    if not puede_aceptar(pregunta, solicitante):
        raise PermissionError(
            "Solo el autor de la pregunta puede aceptar una respuesta."
        )
    for otra in pregunta.respuestas:
        otra.es_aceptada = otra.id == respuesta.id
    db.session.commit()
    return respuesta