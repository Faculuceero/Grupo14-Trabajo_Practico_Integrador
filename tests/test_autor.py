"""Pruebas de Autor (responsable: German Coero Borga)."""
import pytest

from plataforma_qa.autores.agente_ia import AgenteIA
from plataforma_qa.autores.autor import Autor
from plataforma_qa.autores.usuario import Usuario


def test_es_abstracta():
    with pytest.raises(TypeError):
        Autor(1, "Ana")


def test_usuario_y_agente_ia_heredan_de_autor():
    assert issubclass(Usuario, Autor)
    assert issubclass(AgenteIA, Autor)
