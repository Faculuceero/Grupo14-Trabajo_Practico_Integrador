"""Pruebas de Pregunta (responsable: Facu Lucero)."""

from datetime import datetime

import pytest

from plataforma_qa.publicaciones.pregunta import Pregunta
from plataforma_qa.publicaciones.respuesta import Respuesta


def test_guarda_sus_datos(pregunta, usuario, categoria, texto):
    assert pregunta._titulo == "¿Cómo se usa una lista?"
    assert pregunta._autor is usuario
    assert pregunta._categoria is categoria
    assert pregunta._cuerpo is texto
    assert pregunta._etiquetas == []


def test_el_titulo_es_obligatorio(usuario, categoria, texto):
    with pytest.raises(ValueError):
        Pregunta("", texto, datetime.now(), usuario, categoria)


def test_la_categoria_es_obligatoria(usuario, texto):
    with pytest.raises(ValueError):
        Pregunta("Título", texto, datetime.now(), usuario, None)


def test_el_autor_puede_aceptar_una_respuesta(pregunta, usuario, otro_usuario, texto):
    r = Respuesta(texto, datetime.now(), otro_usuario)
    pregunta.agregar_respuesta(r)
    pregunta.aceptar_respuesta(r, usuario)
    assert r._es_aceptada is True


def test_otro_usuario_no_puede_aceptar_una_respuesta(pregunta, otro_usuario, texto):
    r = Respuesta(texto, datetime.now(), otro_usuario)
    pregunta.agregar_respuesta(r)
    with pytest.raises(PermissionError):
        pregunta.aceptar_respuesta(r, otro_usuario)
    assert r._es_aceptada is False
