"""EstrategiaLLM («interface») - Strategy del patrón Strategy

Responsable: Andres Coero Borga
Issue: "Implementar la interfaz EstrategiaLLM"

Cada proveedor de IA (OpenAI, Gemini, modelo local) la implementa a su manera.
"""
from abc import ABC, abstractmethod


class EstrategiaLLM(ABC):
    """Interfaz común para los proveedores de IA (patrón Strategy)."""

    @abstractmethod
    def generar_texto(self, prompt: str) -> str:
        """Recibe un prompt y devuelve el texto generado."""