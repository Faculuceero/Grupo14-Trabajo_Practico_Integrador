"""API JSON de respuestas.

    GET    /api/preguntas/<id>/respuestas   lista de la pregunta            público
    POST   /api/preguntas/<id>/respuestas   responder                       requiere sesión
    GET    /api/respuestas/<id>             detalle                         público
    PATCH  /api/respuestas/<id>             modificar (solo el autor)       requiere sesión
    DELETE /api/respuestas/<id>             borrar (el autor o un admin)    requiere sesión
    POST   /api/respuestas/<id>/aceptar     aceptar (solo el autor de la pregunta)
"""

from flask import Blueprint, g, jsonify, url_for

from plataforma_qa.api.comun import (
    datos_json,
    login_required_api,
    manejar_errores,
    obtener_o_404,
)
from plataforma_qa.models import Pregunta, Respuesta
from plataforma_qa.services import respuestas as servicio
from plataforma_qa.services import votos as votos_service

respuestas_api_bp = Blueprint("respuestas_api", __name__, url_prefix="/api")
manejar_errores(respuestas_api_bp)


def a_dict(respuesta):
    autor = None
    if not respuesta.es_ia and respuesta.autor is not None:
        autor = {"id": respuesta.autor.id, "nombre": respuesta.autor.name}
    return {
        "id": respuesta.id,
        "pregunta_id": respuesta.pregunta_id,
        "cuerpo": respuesta.cuerpo,
        "autor": autor,
        "es_ia": respuesta.es_ia,
        "nombre_autor": respuesta.nombre_autor,
        "es_aceptada": respuesta.es_aceptada,
        "fecha_publicacion": respuesta.fecha_publicacion.isoformat(),
        "puntuacion": votos_service.puntuacion(respuesta),
    }


@respuestas_api_bp.get("/preguntas/<int:pregunta_id>/respuestas")
def listar(pregunta_id):
    pregunta = obtener_o_404(Pregunta, pregunta_id, "la pregunta")
    ordenadas = sorted(
        pregunta.respuestas, key=lambda r: (not r.es_aceptada, r.fecha_publicacion)
    )
    return jsonify([a_dict(r) for r in ordenadas])


@respuestas_api_bp.post("/preguntas/<int:pregunta_id>/respuestas")
@login_required_api
def crear(pregunta_id):
    pregunta = obtener_o_404(Pregunta, pregunta_id, "la pregunta")
    respuesta = servicio.crear_respuesta(pregunta, g.user, datos_json().get("cuerpo"))
    resultado = jsonify(a_dict(respuesta))
    resultado.status_code = 201
    resultado.headers["Location"] = url_for(
        "respuestas_api.detalle", respuesta_id=respuesta.id
    )
    return resultado


@respuestas_api_bp.get("/respuestas/<int:respuesta_id>")
def detalle(respuesta_id):
    return jsonify(a_dict(obtener_o_404(Respuesta, respuesta_id, "la respuesta")))


@respuestas_api_bp.patch("/respuestas/<int:respuesta_id>")
@login_required_api
def modificar(respuesta_id):
    respuesta = obtener_o_404(Respuesta, respuesta_id, "la respuesta")
    servicio.modificar_respuesta(respuesta, g.user, datos_json().get("cuerpo"))
    return jsonify(a_dict(respuesta))


@respuestas_api_bp.delete("/respuestas/<int:respuesta_id>")
@login_required_api
def borrar(respuesta_id):
    servicio.borrar_respuesta(
        obtener_o_404(Respuesta, respuesta_id, "la respuesta"), g.user
    )
    return "", 204


@respuestas_api_bp.post("/respuestas/<int:respuesta_id>/aceptar")
@login_required_api
def aceptar(respuesta_id):
    respuesta = obtener_o_404(Respuesta, respuesta_id, "la respuesta")
    servicio.aceptar_respuesta(respuesta, g.user)
    return jsonify(a_dict(respuesta))