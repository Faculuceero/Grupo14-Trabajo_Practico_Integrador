"""Rol

Responsable: Nico Migliorini
Issue: "Implementar la clase Rol"
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plataforma_qa.autores.tipo_rol import TipoRol


class Rol:
    def __init__(self, tipo: TipoRol) -> None:
        self._tipo = tipo  # -tipo: TipoRol
