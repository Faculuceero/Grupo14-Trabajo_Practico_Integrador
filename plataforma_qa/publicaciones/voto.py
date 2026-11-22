"""Voto

Responsable: Facu Lucero
Issue: "Implementar la clase Voto"

Un voto POSITIVO o NEGATIVO que un Usuario da a una Publicacion.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from plataforma_qa.publicaciones.tipo_voto import TipoVoto

if TYPE_CHECKING:
    from plataforma_qa.autores.usuario import Usuario


class Voto:
    def __init__(self, tipo: TipoVoto, votante: Usuario) -> None:
        self._tipo = tipo          # -tipo: TipoVoto
        self._votante = votante    # relación: votante (Usuario)

    @property
    def tipo(self) -> TipoVoto:
        """Devuelve el tipo de voto (POSITIVO o NEGATIVO)."""
        return self._tipo

    @property
    def votante(self) -> Usuario:
        """Devuelve el usuario que emitió el voto."""
        return self._votante

    def __repr__(self) -> str:
        return f"Voto(tipo={self._tipo}, votante={self._votante})"