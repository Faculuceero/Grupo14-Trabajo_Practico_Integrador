"""Pruebas de Voto (responsable: Facu Lucero)."""
from plataforma_qa.publicaciones.tipo_voto import TipoVoto
from plataforma_qa.publicaciones.voto import Voto


def test_guarda_el_tipo_y_el_votante(usuario):
    voto = Voto(TipoVoto.NEGATIVO, usuario)
    assert voto._tipo is TipoVoto.NEGATIVO
    assert voto._votante is usuario
