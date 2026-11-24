"""Pruebas de TextoEnriquecido (responsable: German Coero Borga)."""

from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido


def test_guarda_el_contenido():
    assert TextoEnriquecido("Hola **mundo**").contenido == "Hola **mundo**"
