"""Pruebas de FabricaUsuario (responsable: Nico Migliorini)."""

import pytest

from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.autores.usuario import Usuario
from plataforma_qa.fabricas.fabrica_usuario import FabricaUsuario
from tests.utils import datos_usuario


def test_crea_un_usuario_con_rol_usuario_general_por_defecto():
    u = FabricaUsuario().crear_autor(datos_usuario())
    assert isinstance(u, Usuario)
    assert u._email == "ana@mail.com"
    assert u._rol._tipo is TipoRol.USUARIO_GENERAL


def test_se_puede_crear_un_admin():
    u = FabricaUsuario().crear_autor(datos_usuario(rol=TipoRol.ADMIN))
    assert u._rol._tipo is TipoRol.ADMIN


def test_la_contrasena_no_se_guarda_en_texto_plano():
    u = FabricaUsuario().crear_autor(datos_usuario(password="secreta"))
    assert u._password_hash != "secreta"
    assert u.autenticar("secreta") is True


def test_faltan_datos_obligatorios():
    datos = datos_usuario()
    del datos["email"]
    with pytest.raises(ValueError):
        FabricaUsuario().crear_autor(datos)


def test_el_email_debe_ser_unico():
    fabrica = FabricaUsuario()
    fabrica.crear_autor(datos_usuario())
    with pytest.raises(ValueError):
        fabrica.crear_autor(datos_usuario(id=2, nombre="Otra Ana"))
