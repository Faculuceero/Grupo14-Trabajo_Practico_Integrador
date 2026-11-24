"""FabricaAutor (clase abstracta) - Creator del patrón Factory Method

Responsable: German Coero Borga
Issue: "Implementar la clase FabricaAutor"
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plataforma_qa.autores.autor import Autor


class FabricaAutor(ABC):
    @abstractmethod
    def crear_autor(self, datos: dict) -> Autor:
        """Método fábrica: cada subclase decide qué tipo de Autor crear.

        Recibe un diccionario con los datos del autor y devuelve un Autor.
        Cada fábrica concreta define qué claves necesita (ver README, sección
        "Acuerdos del equipo") y lanza ValueError si falta alguna.
        """
