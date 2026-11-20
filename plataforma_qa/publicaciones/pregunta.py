"""Pregunta (hereda de Publicacion)

Responsable: Facu Lucero
Issue: "Implementar la clase Pregunta"
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from plataforma_qa.publicaciones.publicacion import Publicacion

if TYPE_CHECKING:
    from plataforma_qa.autores.usuario import Usuario
    from plataforma_qa.publicaciones.categoria import Categoria
    from plataforma_qa.publicaciones.etiqueta import Etiqueta
    from plataforma_qa.publicaciones.respuesta import Respuesta
    from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido


class Pregunta(Publicacion):
    def __init__(self, titulo: str, cuerpo: TextoEnriquecido, fecha_publicacion: datetime,
                 autor: Usuario, categoria: Categoria,
                 etiquetas: list[Etiqueta] | None = None) -> None:
        # TODO: validar que título, cuerpo y categoría existan
        super().__init__(cuerpo, fecha_publicacion)
        self._titulo = titulo                    # -titulo: String
        self._autor = autor                      # relación: autor (Usuario)
        self._categoria = categoria              # relación: exactamente 1 Categoria
        self._etiquetas = etiquetas or []        # relación: 0..* Etiqueta
        self._respuestas: list[Respuesta] = []   # relación: contiene 0..* Respuesta

    def aceptar_respuesta(self, r: Respuesta, solicitante: Usuario) -> None:
        """Solo el autor de la pregunta puede marcar una respuesta como aceptada."""
        raise NotImplementedError

    def agregar_respuesta(self, r: Respuesta) -> None:
        """Método auxiliar (no figura en el diagrama): suma una respuesta a la pregunta."""
        raise NotImplementedError
