"""Agente de IA: responde preguntas de forma automática.

Conecta IAService + FabricaAgenteIA (que crean y usan al agente) con el modelo
Respuesta. Se configura con variables de entorno; nunca hay claves en el código:

    IA_PROVEEDOR        gemini (por defecto) | openai | local
    IA_AGENTE_NOMBRE    nombre que se muestra (por defecto "Asistente IA")
    GEMINI_API_KEY / OPENAI_API_KEY   según el proveedor elegido

Cuándo responde (igual que AgenteIA.debe_responder del dominio):
    - Nunca si la pregunta ya tiene respuestas (así no contesta dos veces).
    - Enseguida si tiene la etiqueta #ia-help.
    - Si no, cuando pasaron N minutos sin que nadie responda.
"""

import logging
import os
from datetime import UTC, datetime, timedelta

from plataforma_qa.estrategias.estrategia_gemini import EstrategiaGemini
from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM
from plataforma_qa.estrategias.estrategia_modelo_local import EstrategiaModeloLocal
from plataforma_qa.estrategias.estrategia_openai import EstrategiaOpenAI
from plataforma_qa.extensions import db
from plataforma_qa.models import Pregunta
from plataforma_qa.services.errores import AgenteIAError, Conflicto
from plataforma_qa.services.ia_service import IAService
from plataforma_qa.services.respuestas import crear_respuesta_ia

logger = logging.getLogger(__name__)

ETIQUETA_IA = "ia-help"
MINUTOS_POR_DEFECTO = 30
AGENTE_ID = 1

# IAService no lanza errores: los devuelve como texto que empieza así.
TEXTOS_DE_ERROR = (
    "No se pudo completar la respuesta del Agente IA",
    "Error de configuración del agente",
)


class _EstrategiaConAlias(EstrategiaLLM):
    """Adapta una estrategia real para IAService.

    IAService llama a estrategia.generar_respuesta(prompt), pero las estrategias
    (Gemini, OpenAI, modelo local) implementan generar_texto(prompt).
    """

    def __init__(self, base: EstrategiaLLM) -> None:
        self._base = base

    def generar_texto(self, prompt: str) -> str:
        return self._base.generar_texto(prompt)

    def generar_respuesta(self, prompt: str) -> str:
        return self.generar_texto(prompt)


def crear_estrategia(proveedor: str | None = None) -> EstrategiaLLM:
    """Elige el proveedor de IA (patrón Strategy) según IA_PROVEEDOR."""
    nombre = (proveedor or os.environ.get("IA_PROVEEDOR", "gemini")).strip().lower()
    estrategias = {
        "gemini": EstrategiaGemini,
        "openai": EstrategiaOpenAI,
        "local": EstrategiaModeloLocal,
    }
    if nombre not in estrategias:
        raise ValueError(
            f"Proveedor de IA desconocido: '{nombre}'. Usá gemini, openai o local."
        )
    return estrategias[nombre]()


def tiene_etiqueta_ia(pregunta) -> bool:
    return any(e.nombre.lstrip("#").lower() == ETIQUETA_IA for e in pregunta.etiquetas)


def debe_responder(pregunta, minutos: int, ahora: datetime | None = None) -> bool:
    if pregunta.respuestas:
        return False
    if tiene_etiqueta_ia(pregunta):
        return True
    ahora = (ahora or datetime.now(UTC)).replace(tzinfo=None)
    publicada = pregunta.fecha_publicacion.replace(tzinfo=None)
    return ahora - publicada >= timedelta(minutes=minutos)


def responder_con_ia(pregunta, minutos=MINUTOS_POR_DEFECTO, estrategia=None):
    """Pide la respuesta al agente y la guarda como respuesta de IA.

    Conflicto si la pregunta ya tiene respuestas; AgenteIAError si el proveedor falla
    (en ese caso no se guarda nada).
    """
    if pregunta.respuestas:
        raise Conflicto("La pregunta ya tiene respuestas.")

    nombre = os.environ.get("IA_AGENTE_NOMBRE", "Asistente IA")
    try:
        base = estrategia or crear_estrategia()
    except ValueError as error:
        raise AgenteIAError(str(error)) from error

    datos_agente = {
        "id": AGENTE_ID,
        "nombre": nombre,
        "etiqueta": ETIQUETA_IA,
        "minutos_sin_respuesta": minutos,
        "estrategia": _EstrategiaConAlias(base),
    }
    contexto = {"titulo": pregunta.titulo, "cuerpo": pregunta.cuerpo}
    texto = IAService().generar_respuesta_automatica(contexto, datos_agente)

    if not texto or not texto.strip() or texto.startswith(TEXTOS_DE_ERROR):
        raise AgenteIAError(texto or "El proveedor no devolvió ningún texto.")
    return crear_respuesta_ia(pregunta, texto, nombre)


def responder_automaticamente(pregunta, estrategia=None):
    """Para preguntas nuevas o editadas: responde solo si tiene #ia-help y está sin responder."""
    if pregunta.respuestas or not tiene_etiqueta_ia(pregunta):
        return None
    return responder_con_ia(pregunta, estrategia=estrategia)


def responder_pendientes(minutos=MINUTOS_POR_DEFECTO, estrategia=None):
    """Responde todas las preguntas pendientes. Devuelve (respondidas, fallidas)."""
    candidatas = db.session.scalars(
        db.select(Pregunta)
        .where(~Pregunta.respuestas.any())
        .order_by(Pregunta.fecha_publicacion, Pregunta.id)
    ).all()

    respondidas, fallidas = [], []
    for pregunta in candidatas:
        if not debe_responder(pregunta, minutos):
            continue
        try:
            respondidas.append(responder_con_ia(pregunta, minutos, estrategia))
        except AgenteIAError as error:
            logger.warning("El agente IA no pudo responder la pregunta %s: %s", pregunta.id, error)
            fallidas.append((pregunta.id, str(error)))
    return respondidas, fallidas