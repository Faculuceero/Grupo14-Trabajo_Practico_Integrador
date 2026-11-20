"""Pruebas de Respuesta (responsable: Facu Lucero)."""
from datetime import datetime

from plataforma_qa.publicaciones.respuesta import Respuesta


def test_no_esta_aceptada_por_defecto(texto, usuario):
    assert Respuesta(texto, datetime.now(), usuario)._es_aceptada is False


def test_el_autor_puede_ser_un_usuario_o_un_agente_ia(texto, usuario, agente):
    assert Respuesta(texto, datetime.now(), usuario)._autor is usuario
    assert Respuesta(texto, datetime.now(), agente)._autor is agente
