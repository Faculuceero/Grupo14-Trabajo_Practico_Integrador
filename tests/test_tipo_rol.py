"""Pruebas de TipoRol (responsable: Nico Migliorini)."""
from plataforma_qa.autores.tipo_rol import TipoRol


def test_tiene_exactamente_dos_valores():
    assert {t.name for t in TipoRol} == {"ADMIN", "USUARIO_GENERAL"}
