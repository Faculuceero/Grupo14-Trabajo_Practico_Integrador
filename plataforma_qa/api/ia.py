"""API JSON del agente de IA.

    POST /api/preguntas/<id>/respuesta-ia   el agente IA responde la pregunta
                                            (requiere sesión; 409 si ya tiene respuestas,
                                            502 si falla el proveedor de IA)
"""

from flask import Blueprint, jsonify, url_for

from plataforma_qa.api.comun import login_required_api, manejar_errores, obtener_o_404
from plataforma_qa.api.respuestas import a_dict as respuesta_a_dict
from plataforma_qa.models import Pregunta
from plataforma_qa.services import agente_ia

ia_api_bp = Blueprint("ia_api", __name__, url_prefix="/api")
manejar_errores(ia_api_bp)


@ia_api_bp.post("/preguntas/<int:pregunta_id>/respuesta-ia")
@login_required_api
def responder(pregunta_id):
    pregunta = obtener_o_404(Pregunta, pregunta_id, "la pregunta")
    respuesta = agente_ia.responder_con_ia(pregunta)
    resultado = jsonify(respuesta_a_dict(respuesta))
    resultado.status_code = 201
    resultado.headers["Location"] = url_for(
        "respuestas_api.detalle", respuesta_id=respuesta.id
    )
    return resultado