"""EstrategiaOpenAI (implementa EstrategiaLLM) - ConcreteStrategy

Responsable: Andres Coero Borga
Issue: "Implementar la clase EstrategiaOpenAI"

Proveedor: OpenAI. La clave de API (si hace falta) se lee de una variable
de entorno y NUNCA se sube al repositorio.
"""
from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM


class EstrategiaOpenAI(EstrategiaLLM):
    def generar_texto(self, prompt: str) -> str:
        raise NotImplementedError
