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

    def _extraer_nombres_etiquetas(self, p: Pregunta) -> list[str]:
        """Extrae el nombre en string de cada objeto Etiqueta en la pregunta."""
        etiquetas_raw = getattr(p, "_etiquetas", getattr(p, "etiquetas", []))
        nombres = []
        for e in etiquetas_raw:
            if hasattr(e, "_nombre"):
                nombres.append(str(e._nombre))
            elif hasattr(e, "nombre"):
                nombres.append(str(e.nombre))
            elif isinstance(e, str):
                nombres.append(e)
            else:
                nombres.append(str(e))
        return nombres

    def debe_responder(self, p: Pregunta) -> bool:
        """Evalúa si la pregunta carece de respuestas y si transcurrió el tiempo configurado."""
        if len(p.respuestas) > 0 or len(getattr(p, "_respuestas", [])) > 0:
            return False

        nombres_etiquetas = self._extraer_nombres_etiquetas(p)
        
        # Si la pregunta tiene la etiqueta del agente, o si no tiene etiquetas pero ya pasó el tiempo
        tiene_etiqueta_agente = self._etiqueta in nombres_etiquetas
        
        minutos_transcurridos = (datetime.now() - p.fecha_publicacion).total_seconds() / 60
        paso_tiempo = minutos_transcurridos >= self._minutos_sin_respuesta

        if tiene_etiqueta_agente:
            return True

        return paso_tiempo

    def debeResponder(self, p: Pregunta) -> bool:
        """Alias camelCase acorde a UML."""
        return self.debe_responder(p)

    def generar_respuesta(self, p: Pregunta) -> Respuesta:
        """Delega la generación del contenido a la estrategia actual y retorna la Respuesta."""
        if self._estrategia is None:
            raise ValueError("No se puede generar una respuesta sin una EstrategiaLLM configurada.")

        # Obtener los nombres limpios en string para incluirlos en el prompt
        nombres_etiquetas = self._extraer_nombres_etiquetas(p)
        etiquetas_str = " ".join(nombres_etiquetas)
        cuerpo_texto = getattr(p.cuerpo, "contenido", str(p.cuerpo))
        
        prompt = f"{p.titulo} {cuerpo_texto} {etiquetas_str}".strip()

        # Delegar a la estrategia según la firma que implemente
        if hasattr(self._estrategia, "generar_texto"):
            texto_respuesta = self._estrategia.generar_texto(prompt)
        elif hasattr(self._estrategia, "generarTexto"):
            texto_respuesta = self._estrategia.generarTexto(prompt)
        else:
            raise AttributeError("La estrategia no implementa un método válido de generación de texto.")

        respuesta = Respuesta(
            cuerpo=TextoEnriquecido(texto_respuesta),
            fecha_publicacion=datetime.now(),
            autor=self
        )

        # Vincular automáticamente la respuesta en la lista interna de la pregunta
        if hasattr(p, "agregar_respuesta"):
            p.agregar_respuesta(respuesta)
        elif hasattr(p, "_respuestas"):
            p._respuestas.append(respuesta)

        return respuesta

    def generarRespuesta(self, p: Pregunta) -> Respuesta:
        """Alias camelCase acorde a UML."""
        return self.generar_respuesta(p)