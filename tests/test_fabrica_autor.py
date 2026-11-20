"""Pruebas de FabricaAutor y del patrón Factory Method (responsable: German Coero Borga)."""
import pytest

from plataforma_qa.autores.autor import Autor
from plataforma_qa.fabricas.fabrica_agente_ia import FabricaAgenteIA
from plataforma_qa.fabricas.fabrica_autor import FabricaAutor
from plataforma_qa.fabricas.fabrica_usuario import FabricaUsuario
from tests.utils import datos_agente, datos_usuario


def test_es_abstracta():
    with pytest.raises(TypeError):
        FabricaAutor()


def test_ambas_fabricas_se_usan_de_la_misma_forma():
    """El código cliente solo conoce FabricaAutor y Autor, no las clases concretas."""
    pedidos = [(FabricaUsuario(), datos_usuario()), (FabricaAgenteIA(), datos_agente())]
    for fabrica, datos in pedidos:
        assert isinstance(fabrica, FabricaAutor)
        assert isinstance(fabrica.crear_autor(datos), Autor)
