"""Pruebas de Etiqueta (responsable: German Coero Borga)."""
import pytest

from plataforma_qa.publicaciones.etiqueta import Etiqueta


def test_guarda_el_nombre():
    assert Etiqueta("Python")._nombre == "Python"


def test_no_permite_nombre_vacio():
    with pytest.raises(ValueError):
        Etiqueta("")
