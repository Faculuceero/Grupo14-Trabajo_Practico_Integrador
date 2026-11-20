"""Pruebas de EstrategiaGemini (responsable: Andres Coero Borga).

No se hacen llamadas reales a internet. Variables de entorno esperadas: GEMINI_API_KEY, GOOGLE_API_KEY.
"""
import pytest

from plataforma_qa.estrategias.estrategia_gemini import EstrategiaGemini


def test_sin_clave_de_api_informa_un_error_claro(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as info:
        EstrategiaGemini().generar_texto("hola")
    assert not isinstance(info.value, NotImplementedError)
