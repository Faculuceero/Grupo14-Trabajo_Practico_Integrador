"""FabricaUsuario (hereda de FabricaAutor) - ConcreteCreator

Responsable: Nico Migliorini
Issue: "Implementar la clase FabricaUsuario"
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from plataforma_qa.fabricas.fabrica_autor import FabricaAutor

if TYPE_CHECKING:
    from plataforma_qa.autores.usuario import Usuario


class FabricaUsuario(FabricaAutor):
    def crear_autor(self, datos: dict) -> Usuario:
        raise NotImplementedError
