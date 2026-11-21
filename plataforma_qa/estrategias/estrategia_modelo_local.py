"""EstrategiaModeloLocal (implementa EstrategiaLLM) - ConcreteStrategy

Responsable: Andres Coero Borga
Issue: "Implementar la clase EstrategiaModeloLocal"

Proveedor: un modelo local. La clave de API (si hace falta) se lee de una variable
de entorno y NUNCA se sube al repositorio.
"""
import json
import urllib.error
import urllib.request

from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM


class EstrategiaModeloLocal(EstrategiaLLM):
    def __init__(
        self,
        direccion: str = "http://localhost:11434",
        modelo: str = "llama3.2",
        timeout: int = 60,
    ):
        self._direccion = direccion.rstrip("/")
        self._modelo = modelo
        self._timeout = timeout

    def generar_texto(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError("El prompt debe ser un string.")
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        cuerpo = json.dumps({
            "model": self._modelo,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")
        pedido = urllib.request.Request(
            f"{self._direccion}/api/generate",
            data=cuerpo,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            return datos["response"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(
                f"El modelo local respondió con error HTTP {e.code}."
            ) from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise RuntimeError(
                f"El modelo local no está disponible en {self._direccion}."
            ) from e
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            raise RuntimeError("Respuesta inesperada del modelo local.") from e