"""TextoEnriquecido («dataType»)

Responsable: German Coero Borga
Issue: "Implementar la clase TextoEnriquecido"

Texto con formato que se usa como cuerpo de preguntas y respuestas.
"""


class TextoEnriquecido:
    """Texto con formato (por ejemplo Markdown o HTML) para el cuerpo de preguntas y respuestas."""

    def __init__(self, contenido: str) -> None:
        self.contenido = contenido  # +contenido: String

    def __str__(self) -> str:
        return self.contenido
