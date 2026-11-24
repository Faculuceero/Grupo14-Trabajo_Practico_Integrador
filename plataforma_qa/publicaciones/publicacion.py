"""Publicacion (clase abstracta)

Responsable: Facu Lucero
Issue: "Implementar la clase Publicacion"

Clase base de Pregunta y Respuesta. Guarda el cuerpo, la fecha y los votos.
"""

from __future__ import annotations

from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido
    from plataforma_qa.publicaciones.voto import Voto


class Publicacion(ABC):
    def __init__(self, cuerpo: TextoEnriquecido, fecha_publicacion: datetime) -> None:
        if type(self) is Publicacion:
            raise TypeError(
                "No se puede instanciar directamente la clase abstracta Publicacion."
            )

        self._cuerpo = cuerpo  # #cuerpo: TextoEnriquecido
        self._fecha_publicacion = fecha_publicacion  # #fechaPublicacion: Date
        self._votos: list[Voto] = []  # relación: 1 Publicacion - 0..* Voto

    @property
    def cuerpo(self) -> TextoEnriquecido:
        return self._cuerpo

    @property
    def fecha_publicacion(self) -> datetime:
        return self._fecha_publicacion

    @property
    def votos(self) -> list[Voto]:
        return self._votos

    def agregar_voto(self, voto: Voto) -> None:
        """Método auxiliar: registra un voto recibido."""
        self._votos.append(voto)

    def calcular_puntuacion(self) -> int:
        """votos POSITIVOS menos votos NEGATIVOS (0 si no hay votos)."""
        from plataforma_qa.publicaciones.tipo_voto import TipoVoto

        positivos = sum(1 for v in self._votos if v.tipo == TipoVoto.POSITIVO)
        negativos = sum(1 for v in self._votos if v.tipo == TipoVoto.NEGATIVO)
        return positivos - negativos

    def calcularPuntuacion(self) -> int:
        """Alias en camelCase según diagrama UML."""
        return self.calcular_puntuacion()
