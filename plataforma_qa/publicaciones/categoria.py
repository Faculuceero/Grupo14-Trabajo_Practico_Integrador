"""Categoria

Responsable: German Coero Borga
Issue: "Implementar la clase Categoria"

Cada Pregunta pertenece a exactamente una Categoria (ej: Python, Flask).
"""


class Categoria:
    def __init__(self, nombre: str) -> None:
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        self._nombre = nombre  # -nombre: String
