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
        # TODO: impedir que se instancie directamente (es abstracta)
        self._cuerpo = cuerpo                          # #cuerpo: TextoEnriquecido
        self._fecha_publicacion = fecha_publicacion    # #fechaPublicacion: Date
        self._votos: list[Voto] = []                   # relación: 1 Publicacion - 0..* Voto

    def calcular_puntuacion(self) -> int:
        """votos POSITIVOS menos votos NEGATIVOS (0 si no hay votos)."""
        raise NotImplementedError

    def agregar_voto(self, voto: Voto) -> None:
        """Método auxiliar (no figura en el diagrama): registra un voto recibido."""
        raise NotImplementedError
