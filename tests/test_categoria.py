"""Pruebas de Categoria (responsable: German Coero Borga)."""

import pytest

from plataforma_qa.publicaciones.categoria import Categoria


def test_guarda_el_nombre():
    assert Categoria("Python")._nombre == "Python"


def test_no_permite_nombre_vacio():
    with pytest.raises(ValueError):
        Categoria("")
