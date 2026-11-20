"""Etiqueta

Responsable: German Coero Borga
Issue: "Implementar la clase Etiqueta"

Una Pregunta puede tener varias Etiquetas, o ninguna (ej: ia-help).
"""


class Etiqueta:
    def __init__(self, nombre: str) -> None:
        # TODO: no permitir un nombre vacío
        self._nombre = nombre  # -nombre: String
