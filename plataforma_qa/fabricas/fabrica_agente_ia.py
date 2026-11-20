"""FabricaAgenteIA (hereda de FabricaAutor) - ConcreteCreator

Responsable: Nico Migliorini
Issue: "Implementar la clase FabricaAgenteIA"
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from plataforma_qa.fabricas.fabrica_autor import FabricaAutor

if TYPE_CHECKING:
    from plataforma_qa.autores.agente_ia import AgenteIA


class FabricaAgenteIA(FabricaAutor):
    def crear_autor(self, datos: dict) -> AgenteIA:
        raise NotImplementedError
