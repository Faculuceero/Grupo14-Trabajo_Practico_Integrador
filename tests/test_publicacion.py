"""Pruebas de Publicacion (responsable: Facu Lucero)."""

from datetime import datetime

import pytest

from plataforma_qa.publicaciones.publicacion import Publicacion
from plataforma_qa.publicaciones.tipo_voto import TipoVoto
from plataforma_qa.publicaciones.voto import Voto
from tests.utils import crear_usuario


class PublicacionConcreta(Publicacion):
    """Subclase mínima, solo para poder probar la clase abstracta."""


def test_es_abstracta(texto):
    with pytest.raises(TypeError):
        Publicacion(texto, datetime.now())


def test_sin_votos_la_puntuacion_es_cero(texto):
    assert PublicacionConcreta(texto, datetime.now()).calcular_puntuacion() == 0


def test_la_puntuacion_es_positivos_menos_negativos(texto):
    pub = PublicacionConcreta(texto, datetime.now())
    pub.agregar_voto(Voto(TipoVoto.POSITIVO, crear_usuario(1)))
    pub.agregar_voto(Voto(TipoVoto.POSITIVO, crear_usuario(2)))
    pub.agregar_voto(Voto(TipoVoto.NEGATIVO, crear_usuario(3)))
    assert pub.calcular_puntuacion() == 1
