"""API JSON de preguntas: /api/preguntas

    GET    /api/preguntas        lista (filtros ?categoria_id= y ?etiqueta=)   público
    GET    /api/preguntas/<id>   detalle                                       público
    POST   /api/preguntas        crear                       requiere sesión
    PATCH  /api/preguntas/<id>   modificar (solo el autor)   requiere sesión
    DELETE /api/preguntas/<id>   borrar (solo el autor)      requiere sesión
"""

from flask import Blueprint, g, jsonify, request, url_for

from plataforma_qa.api.comun import (
    datos_json,
    login_required_api,
    manejar_errores,
    obtener_o_404,
)
from plataforma_qa.models import Pregunta
from plataforma_qa.services import preguntas as servicio
from plataforma_qa.services import votos as votos_service

preguntas_api_bp = Blueprint("preguntas_api", __name__, url_prefix="/api/preguntas")
manejar_errores(preguntas_api_bp)


def a_dict(pregunta):
    """Solo datos públicos: nunca el email ni la contraseña del autor."""
    return {
        "id": pregunta.id,
        "titulo": pregunta.titulo,
        "cuerpo": pregunta.cuerpo,
        "categoria": {"id": pregunta.categoria.id, "nombre": pregunta.categoria.nombre},
        "etiquetas": [e.nombre for e in pregunta.etiquetas],
        "autor": {"id": pregunta.autor.id, "nombre": pregunta.autor.name},
        "fecha_publicacion": pregunta.fecha_publicacion.isoformat(),
        "puntuacion": votos_service.puntuacion(pregunta),
        "cantidad_respuestas": len(pregunta.respuestas),
    }


@preguntas_api_bp.get("")
def listar():
    preguntas = servicio.listar_preguntas(
        categoria_id=request.args.get("categoria_id", type=int),
        etiqueta=request.args.get("etiqueta"),
    )
    return jsonify([a_dict(p) for p in preguntas])


@preguntas_api_bp.get("/<int:pregunta_id>")
def detalle(pregunta_id):
    return jsonify(a_dict(obtener_o_404(Pregunta, pregunta_id, "la pregunta")))


@preguntas_api_bp.post("")
@login_required_api
def crear():
    datos = datos_json()
    pregunta = servicio.crear_pregunta(
        g.user,
        datos.get("titulo"),
        datos.get("cuerpo"),
        datos.get("categoria_id"),
        datos.get("etiquetas"),
    )
    respuesta = jsonify(a_dict(pregunta))
    respuesta.status_code = 201
    respuesta.headers["Location"] = url_for(
        "preguntas_api.detalle", pregunta_id=pregunta.id
    )
    return respuesta


@preguntas_api_bp.patch("/<int:pregunta_id>")
@login_required_api
def modificar(pregunta_id):
    pregunta = obtener_o_404(Pregunta, pregunta_id, "la pregunta")
    datos = datos_json()
    servicio.modificar_pregunta(
        pregunta,
        g.user,
        titulo=datos.get("titulo"),
        cuerpo=datos.get("cuerpo"),
        categoria_id=datos.get("categoria_id"),
        etiquetas=datos.get("etiquetas"),
    )
    return jsonify(a_dict(pregunta))


@preguntas_api_bp.delete("/<int:pregunta_id>")
@login_required_api
def borrar(pregunta_id):
    servicio.borrar_pregunta(
        obtener_o_404(Pregunta, pregunta_id, "la pregunta"), g.user
    )
    return "", 204