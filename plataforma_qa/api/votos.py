"""API JSON de votos.

    POST /api/preguntas/<id>/votos    {"valor": 1 | -1}   requiere sesión
    POST /api/respuestas/<id>/votos   {"valor": 1 | -1}   requiere sesión

Votar lo contrario cambia el voto; votar lo mismo otra vez lo retira.
Responde con la puntuación resultante: {"puntuacion": n}.
"""

from flask import Blueprint, g, jsonify

from plataforma_qa.api.comun import (
    datos_json,
    login_required_api,
    manejar_errores,
    obtener_o_404,
)
from plataforma_qa.models import Pregunta, Respuesta
from plataforma_qa.services import votos as servicio

votos_api_bp = Blueprint("votos_api", __name__, url_prefix="/api")
manejar_errores(votos_api_bp)


@votos_api_bp.post("/preguntas/<int:pregunta_id>/votos")
@login_required_api
def votar_pregunta(pregunta_id):
    pregunta = obtener_o_404(Pregunta, pregunta_id, "la pregunta")
    return jsonify({"puntuacion": servicio.votar(pregunta, g.user, datos_json().get("valor"))})


@votos_api_bp.post("/respuestas/<int:respuesta_id>/votos")
@login_required_api
def votar_respuesta(respuesta_id):
    respuesta = obtener_o_404(Respuesta, respuesta_id, "la respuesta")
    return jsonify({"puntuacion": servicio.votar(respuesta, g.user, datos_json().get("valor"))})