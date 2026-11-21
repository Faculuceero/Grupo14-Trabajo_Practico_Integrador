"""AgenteIA (hereda de Autor) - Contexto del patrón Strategy

Responsable: Facu Lucero
Issue: "Implementar la clase AgenteIA"

Solo debe conocer la interfaz EstrategiaLLM, nunca a un proveedor concreto.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from plataforma_qa.autores.autor import Autor
from plataforma_qa.publicaciones.respuesta import Respuesta
from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido

if TYPE_CHECKING:
    from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM
    from plataforma_qa.publicaciones.pregunta import Pregunta


class AgenteIA(Autor):
    def __init__(self, id: int, nombre_visible: str, etiqueta: str,
                 minutos_sin_respuesta: int, estrategia: EstrategiaLLM | None = None) -> None:
        super().__init__(id, nombre_visible)
        self._etiqueta = etiqueta                            # -etiqueta: String (ej: "ia-help")
        self._minutos_sin_respuesta = minutos_sin_respuesta  # -minutosSinRespuesta: int
        self._estrategia = estrategia                        # relación: 1 EstrategiaLLM

    @property
    def etiqueta(self) -> str:
        return self._etiqueta

    @property
    def minutos_sin_respuesta(self) -> int:
        return self._minutos_sin_respuesta

    @property
    def estrategia(self) -> EstrategiaLLM | None:
        return self._estrategia

    def set_estrategia(self, e: EstrategiaLLM) -> None:
        """Asigna o cambia la estrategia LLM dinámicamente."""
        if e is None:
            raise ValueError("La estrategia no puede ser nula.")
        self._estrategia = e

    def setEstrategia(self, e: EstrategiaLLM) -> None:
        """Alias camelCase acorde a UML."""
        self.set_estrategia(e)

    def debe_responder(self, p: Pregunta) -> bool:
        """Evalúa si la pregunta carece de respuestas y si transcurrió el tiempo configurado."""
        if len(p.respuestas) > 0:
            return False

        minutos_transcurridos = (datetime.now() - p.fecha_publicacion).total_seconds() / 60
        return minutos_transcurridos >= self._minutos_sin_respuesta

    def debeResponder(self, p: Pregunta) -> bool:
        """Alias camelCase acorde a UML."""
        return self.debe_responder(p)

    def generar_respuesta(self, p: Pregunta) -> Respuesta:
        """Delega la generación del contenido a la estrategia actual y retorna la Respuesta."""
        if self._estrategia is None:
            raise ValueError("No se puede generar una respuesta sin una EstrategiaLLM configurada.")

        prompt = f"Título: {p.titulo}\nContenido: {p.cuerpo.contenido}"
        texto_respuesta = self._estrategia.generarTexto(prompt)
        
        return Respuesta(
            cuerpo=TextoEnriquecido(texto_respuesta),
            fecha_publicacion=datetime.now(),
            autor=self
        )

    def generarRespuesta(self, p: Pregunta) -> Respuesta:
        """Alias camelCase acorde a UML."""
        return self.generar_respuesta(p)