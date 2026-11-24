"""Pruebas de EstrategiaLLM, interfaz del patrón Strategy (responsable: Andres Coero Borga)."""

import pytest

from plataforma_qa.estrategias.estrategia_gemini import EstrategiaGemini
from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM
from plataforma_qa.estrategias.estrategia_modelo_local import EstrategiaModeloLocal
from plataforma_qa.estrategias.estrategia_openai import EstrategiaOpenAI


def test_es_una_interfaz_y_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        EstrategiaLLM()


def test_los_tres_proveedores_la_implementan():
    for clase in (EstrategiaOpenAI, EstrategiaGemini, EstrategiaModeloLocal):
        assert issubclass(clase, EstrategiaLLM)
