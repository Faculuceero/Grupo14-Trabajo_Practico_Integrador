"""Pruebas de Usuario (responsable: Nico Migliorini)."""

import pytest

from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.autores.usuario import Usuario
from plataforma_qa.publicaciones.pregunta import Pregunta
from plataforma_qa.publicaciones.respuesta import Respuesta
from plataforma_qa.publicaciones.tipo_voto import TipoVoto
from tests.utils import hash_password


@pytest.mark.parametrize("email", ["", "sin-arroba"])
def test_el_email_es_obligatorio_y_debe_ser_valido(email):
    with pytest.raises(ValueError):
        Usuario(1, "Ana", email, hash_password("x"), Rol(TipoRol.USUARIO_GENERAL))


def test_autenticar(usuario):
    assert usuario.autenticar("secreta") is True
    assert usuario.autenticar("otra") is False


def test_preguntar_crea_una_pregunta_del_usuario(usuario, categoria, texto):
    p = usuario.preguntar("¿Qué es una clase?", texto, categoria, [])
    assert isinstance(p, Pregunta)
    assert p._autor is usuario
    assert p._categoria is categoria


def test_responder_crea_una_respuesta_asociada_a_la_pregunta(
    pregunta, otro_usuario, texto
):
    r = otro_usuario.responder(pregunta, texto)
    assert isinstance(r, Respuesta)
    assert r._autor is otro_usuario
    assert r in pregunta._respuestas


def test_votar_actualiza_la_puntuacion(pregunta, otro_usuario):
    otro_usuario.votar(pregunta, TipoVoto.POSITIVO)
    assert pregunta.calcular_puntuacion() == 1


def test_no_se_puede_votar_dos_veces_la_misma_publicacion(pregunta, otro_usuario):
    otro_usuario.votar(pregunta, TipoVoto.POSITIVO)
    with pytest.raises(ValueError):
        otro_usuario.votar(pregunta, TipoVoto.POSITIVO)
