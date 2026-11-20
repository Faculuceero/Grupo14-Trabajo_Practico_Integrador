"""Categoria

Responsable: German Coero Borga
Issue: "Implementar la clase Categoria"

Cada Pregunta pertenece a exactamente una Categoria (ej: Python, Flask).
"""


class Categoria:
    def __init__(self, nombre: str) -> None:
        # TODO: no permitir un nombre vacío
        self._nombre = nombre  # -nombre: String
