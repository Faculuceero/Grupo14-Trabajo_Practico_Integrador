"""EstrategiaGemini (implementa EstrategiaLLM) - ConcreteStrategy

Responsable: Andres Coero Borga
Issue: "Implementar la clase EstrategiaGemini"

Proveedor: Gemini. La clave de API (si hace falta) se lee de una variable
de entorno y NUNCA se sube al repositorio.
"""
import json
import os
import urllib.error
import urllib.request

from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM


class EstrategiaGemini(EstrategiaLLM):
    URL = "https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent"

    def __init__(self, modelo: str = "gemini-2.5-flash", timeout: int = 30):
        self._modelo = modelo
        self._timeout = timeout

    def generar_texto(self, prompt: str) -> str:
        if not isinstance(prompt, str):
            raise TypeError("El prompt debe ser un string.")
        if not prompt.strip():
            raise ValueError("El prompt no puede estar vacío.")

        api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Falta la variable de entorno GEMINI_API_KEY (o GOOGLE_API_KEY)."
            )

        cuerpo = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
        }).encode("utf-8")
        pedido = urllib.request.Request(
            self.URL.format(modelo=self._modelo),
            data=cuerpo,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(pedido, timeout=self._timeout) as respuesta:
                datos = json.loads(respuesta.read().decode("utf-8"))
            return datos["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Gemini respondió con error HTTP {e.code}.") from e
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            raise RuntimeError("No se pudo conectar con Gemini.") from e
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as e:
            raise RuntimeError("Respuesta inesperada de Gemini.") from e