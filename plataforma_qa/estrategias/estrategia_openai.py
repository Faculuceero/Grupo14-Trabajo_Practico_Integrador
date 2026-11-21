"""EstrategiaOpenAI (implementa EstrategiaLLM) - ConcreteStrategy

Responsable: Andres Coero Borga
Issue: "Implementar la clase EstrategiaOpenAI"

Proveedor: OpenAI. La clave de API (si hace falta) se lee de una variable
de entorno y NUNCA se sube al repositorio.
"""
import json
import os
import urllib.error
import urllib.request

from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM


class EstrategiaOpenAI(EstrategiaLLM):
    URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, modelo: str = "gpt-4o-mini", timeout: int = 30):
        self._modelo = modelo
        self._timeout = timeout

    def generar_texto(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError("El prompt debe ser un string.")
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable de entorno OPENAI_API_KEY.")

        cuerpo = json.dumps({
            "model": self._modelo,
            "messages": [{"role": "user", "content": prompt}],
        }).encode("utf-8")
        pedido = urllib.request.Request(
            self.URL,
            data=cuerpo,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            return datos["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"OpenAI respondió con error HTTP {e.code}.") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise RuntimeError("No se pudo conectar con OpenAI.") from e
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
            raise RuntimeError("Respuesta inesperada de OpenAI.") from e