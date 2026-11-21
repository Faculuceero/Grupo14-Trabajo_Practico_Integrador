"""Respuesta (hereda de Publicacion)

Responsable: Facu Lucero
Issue: "Implementar la clase Respuesta"

Su autor puede ser un Usuario o un AgenteIA: esta clase solo conoce a Autor.
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from plataforma_qa.publicaciones.publicacion import Publicacion

if TYPE_CHECKING:
    from plataforma_qa.autores.autor import Autor
    from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido


class Respuesta(Publicacion):
    def __init__(self, cuerpo: TextoEnriquecido, fecha_publicacion: datetime,
                 autor: Autor) -> None:
        super().__init__(cuerpo, fecha_publicacion)
        self._autor = autor              # relación: autor (Autor)
        self._es_aceptada = False        # -esAceptada: bool

    @property
    def autor(self) -> Autor:
        return self._autor

    @property
    def es_aceptada(self) -> bool:
        return self._es_aceptada

    @es_aceptada.setter
    def es_aceptada(self, valor: bool) -> None:
        self._es_aceptada = valor

    def esAceptada(self) -> bool:
        """Getter estilo camelCase por UML."""
        return self._es_aceptada

    def calcular_puntuacion(self) -> int:
        from plataforma_qa.publicaciones.tipo_voto import TipoVoto

        positivos = sum(1 for v in self._votos if v.tipo == TipoVoto.POSITIVO)
        negativos = sum(1 for v in self._votos if v.tipo == TipoVoto.NEGATIVO)
        return positivos - negativos