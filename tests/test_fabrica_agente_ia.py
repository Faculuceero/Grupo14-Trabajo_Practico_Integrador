"""Pruebas de FabricaAgenteIA (responsable: Nico Migliorini)."""
import pytest

from plataforma_qa.autores.agente_ia import AgenteIA
from plataforma_qa.fabricas.fabrica_agente_ia import FabricaAgenteIA
from tests.utils import EstrategiaFalsa, datos_agente


def test_crea_un_agente_ia():
    estrategia = EstrategiaFalsa()
    a = FabricaAgenteIA().crear_autor(datos_agente(estrategia=estrategia))
    assert isinstance(a, AgenteIA)
    assert a._etiqueta == "ia-help"
    assert a._minutos_sin_respuesta == 30
    assert a._estrategia is estrategia


def test_faltan_datos_obligatorios():
    datos = datos_agente()
    del datos["estrategia"]
    with pytest.raises(ValueError):
        FabricaAgenteIA().crear_autor(datos)
