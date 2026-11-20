"""AgenteIA (hereda de Autor) - Contexto del patrón Strategy

Responsable: Facu Lucero
Issue: "Implementar la clase AgenteIA"

Solo debe conocer la interfaz EstrategiaLLM, nunca a un proveedor concreto.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from plataforma_qa.autores.autor import Autor

if TYPE_CHECKING:
    from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM
    from plataforma_qa.publicaciones.pregunta import Pregunta
    from plataforma_qa.publicaciones.respuesta import Respuesta


class AgenteIA(Autor):
    def __init__(self, id: int, nombre_visible: str, etiqueta: str,
                 minutos_sin_respuesta: int, estrategia: EstrategiaLLM | None = None) -> None:
        super().__init__(id, nombre_visible)
        self._etiqueta = etiqueta                            # -etiqueta: String (ej: "ia-help")
        self._minutos_sin_respuesta = minutos_sin_respuesta  # -minutosSinRespuesta: int
        self._estrategia = estrategia                        # relación: 1 EstrategiaLLM

    def set_estrategia(self, e: EstrategiaLLM) -> None:
        raise NotImplementedError

    def generar_respuesta(self, p: Pregunta) -> Respuesta:
        raise NotImplementedError

    def debe_responder(self, p: Pregunta) -> bool:
        raise NotImplementedError
