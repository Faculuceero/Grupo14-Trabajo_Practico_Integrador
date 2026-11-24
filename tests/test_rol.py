"""Pruebas de Rol (responsable: Nico Migliorini)."""

from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol


def test_guarda_el_tipo():
    assert Rol(TipoRol.ADMIN)._tipo is TipoRol.ADMIN
