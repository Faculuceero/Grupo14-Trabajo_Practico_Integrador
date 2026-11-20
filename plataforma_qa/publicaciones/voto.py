"""Voto

Responsable: Facu Lucero
Issue: "Implementar la clase Voto"

Un voto POSITIVO o NEGATIVO que un Usuario da a una Publicacion.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plataforma_qa.autores.usuario import Usuario
    from plataforma_qa.publicaciones.tipo_voto import TipoVoto


class Voto:
    def __init__(self, tipo: TipoVoto, votante: Usuario) -> None:
        self._tipo = tipo          # -tipo: TipoVoto
        self._votante = votante    # relación: votante (Usuario)
