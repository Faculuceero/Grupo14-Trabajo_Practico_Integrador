"""Pruebas de TipoVoto (responsable: Andres Coero Borga)."""
from plataforma_qa.publicaciones.tipo_voto import TipoVoto


def test_tiene_exactamente_dos_valores():
    assert {t.name for t in TipoVoto} == {"POSITIVO", "NEGATIVO"}
