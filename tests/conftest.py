"""Fixtures compartidas: objetos listos para usar en los tests."""

from datetime import datetime

import pytest

from plataforma_qa.autores.agente_ia import AgenteIA
from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.autores.usuario import Usuario
from plataforma_qa.publicaciones.categoria import Categoria
from plataforma_qa.publicaciones.etiqueta import Etiqueta
from plataforma_qa.publicaciones.pregunta import Pregunta
from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido
from tests.utils import EstrategiaFalsa, hash_password


@pytest.fixture
def texto():
    return TextoEnriquecido("Contenido de prueba")


@pytest.fixture
def categoria():
    return Categoria("Python")


@pytest.fixture
def usuario():
    return Usuario(
        1, "Ana", "ana@mail.com", hash_password("secreta"), Rol(TipoRol.USUARIO_GENERAL)
    )


@pytest.fixture
def otro_usuario():
    return Usuario(
        2, "Beto", "beto@mail.com", hash_password("clave"), Rol(TipoRol.USUARIO_GENERAL)
    )


@pytest.fixture
def pregunta(usuario, categoria, texto):
    """Pregunta reciente, sin etiquetas y sin respuestas."""
    return Pregunta(
        "¿Cómo se usa una lista?", texto, datetime.now(), usuario, categoria
    )


@pytest.fixture
def pregunta_ia(usuario, categoria, texto):
    """Pregunta reciente marcada con la etiqueta ia-help."""
    return Pregunta(
        "¿Cómo se usa un diccionario?",
        texto,
        datetime.now(),
        usuario,
        categoria,
        [Etiqueta("ia-help")],
    )


@pytest.fixture
def estrategia():
    return EstrategiaFalsa()


@pytest.fixture
def agente(estrategia):
    """Agente de IA que responde con etiqueta ia-help o tras 30 minutos sin respuestas."""
    return AgenteIA(99, "Asistente IA", "ia-help", 30, estrategia)
