"""Pregunta (hereda de Publicacion)

Responsable: Facu Lucero
Issue: "Implementar la clase Pregunta"
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from plataforma_qa.publicaciones.publicacion import Publicacion
from plataforma_qa.publicaciones.tipo_voto import TipoVoto

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
        
        if not titulo or not titulo.strip():
            raise ValueError("El título de la pregunta no puede estar vacío.")
        if cuerpo is None:
            raise ValueError("El cuerpo de la pregunta es obligatorio.")
        if categoria is None:
            raise ValueError("La categoría es obligatoria.")
        if autor is None:
            raise ValueError("El autor es obligatorio.")

        super().__init__(cuerpo, fecha_publicacion)
        self._titulo = titulo                    # -titulo: String
        self._autor = autor                      # relación: autor (Usuario)
        self._categoria = categoria              # relación: exactamente 1 Categoria
        self._etiquetas = etiquetas or []        # relación: 0..* Etiqueta
        self._respuestas: list[Respuesta] = []   # relación: contiene 0..* Respuesta

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def autor(self) -> Usuario:
        return self._autor

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def etiquetas(self) -> list[Etiqueta]:
        return self._etiquetas

    @property
    def respuestas(self) -> list[Respuesta]:
        return self._respuestas

    def aceptar_respuesta(self, r: Respuesta, solicitante: Usuario) -> None:
        """Solo el autor de la pregunta puede marcar una respuesta como aceptada."""
        if solicitante != self._autor:
            raise PermissionError("Solo el autor de la pregunta puede aceptar una respuesta.")
        if r not in self._respuestas:
            raise ValueError("La respuesta no pertenece a esta pregunta.")

        for resp in self._respuestas:
            resp.es_aceptada = False

        r.es_aceptada = True

    def aceptarRespuesta(self, r: Respuesta, solicitante: Usuario) -> None:
        """Alias camelCase acorde a UML."""
        self.aceptar_respuesta(r, solicitante)

    def agregar_respuesta(self, r: Respuesta) -> None:
        """Suma una respuesta a la lista de respuestas de la pregunta."""
        if r not in self._respuestas:
            self._respuestas.append(r)

    def calcular_puntuacion(self) -> int:
        positivos = sum(1 for v in self._votos if v.tipo == TipoVoto.POSITIVO)
        negativos = sum(1 for v in self._votos if v.tipo == TipoVoto.NEGATIVO)
        return positivos - negativos
