"""Rol

Responsable: Nico Migliorini
Issue: "Implementar la clase Rol"
"""

from __future__ import annotations

from plataforma_qa.autores.tipo_rol import TipoRol


class Rol:
    def __init__(self, tipo: TipoRol = TipoRol.USUARIO_GENERAL) -> None:
        if not isinstance(tipo, TipoRol):
            raise TypeError("El tipo debe ser una instancia de TipoRol")
        self._tipo = tipo  # -tipo: TipoRol

    @property
    def tipo(self) -> TipoRol:
        return self._tipo

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rol):
            return NotImplemented
        return self._tipo == other._tipo

    def __repr__(self) -> str:
        return f"Rol(tipo={self._tipo})"