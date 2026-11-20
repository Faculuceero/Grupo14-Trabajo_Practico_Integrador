"""Pruebas de EstrategiaOpenAI (responsable: Andres Coero Borga).

No se hacen llamadas reales a internet. Variables de entorno esperadas: OPENAI_API_KEY.
"""
import pytest

from plataforma_qa.estrategias.estrategia_openai import EstrategiaOpenAI


def test_sin_clave_de_api_informa_un_error_claro(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError) as info:
        EstrategiaOpenAI().generar_texto("hola")
    assert not isinstance(info.value, NotImplementedError)
