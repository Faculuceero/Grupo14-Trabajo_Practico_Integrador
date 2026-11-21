"""Etiqueta

Responsable: German Coero Borga
Issue: "Implementar la clase Etiqueta"

Una Pregunta puede tener varias Etiquetas, o ninguna (ej: ia-help).
"""


class Etiqueta:
    def __init__(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la etiqueta no puede estar vacío.")
        self._nombre = nombre  # -nombre: String
