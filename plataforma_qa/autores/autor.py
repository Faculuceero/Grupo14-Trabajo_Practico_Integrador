"""Autor (clase abstracta)

Responsable: German Coero Borga
Issue: "Implementar la clase Autor"

Clase base de Usuario y AgenteIA. Gracias a ella, una Respuesta puede ser
escrita por una persona o por la IA sin saber cuál de las dos es.
"""
from abc import ABC


class Autor(ABC):
    def __init__(self, id: int, nombre_visible: str) -> None:
        if type(self) is Autor:
            raise TypeError("Autor es abstracta: no se puede instanciar directamente.")
        self._id = id                            # #id: Int
        self._nombre_visible = nombre_visible    # #nombreVisible: String
