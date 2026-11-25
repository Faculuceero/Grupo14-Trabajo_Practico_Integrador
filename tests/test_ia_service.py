from unittest.mock import MagicMock

import pytest

from plataforma_qa.services.ia_service import IAService


def test_generar_respuesta_con_mock_exitoso():
    mock_estrategia = MagicMock()
    mock_estrategia.generar_respuesta.return_value = (
        "Esta es una respuesta simulada por Mock."
    )

    mock_agente = MagicMock()
    mock_agente.nombre_visible = "Bot-IA"
    mock_agente.estrategia = mock_estrategia

    mock_fabrica = MagicMock()
    mock_fabrica.crear_autor.return_value = mock_agente

    servicio = IAService(fabrica_agente=mock_fabrica)

    contexto = {
        "titulo": "¿Qué es la arquitectura WSGI?",
        "cuerpo": "Necesito una breve explicación para el taller de software.",
    }
    datos_agente = {
        "id": 1,
        "nombre": "Bot-IA",
        "etiqueta": "#ia-help",
        "estrategia": "Gemini",
    }

    resultado = servicio.generar_respuesta_automatica(contexto, datos_agente)

    assert resultado == "Esta es una respuesta simulada por Mock."
    mock_fabrica.crear_autor.assert_called_once_with(datos_agente)
    mock_estrategia.generar_respuesta.assert_called_once()


def test_generar_respuesta_valida_contexto_incompleto():
    servicio = IAService()

    with pytest.raises(
        ValueError,
        match="El contexto de la pregunta debe incluir 'titulo' y 'cuerpo'",
    ):
        servicio.generar_respuesta_automatica({"titulo": ""}, {"id": 1})


def test_manejo_de_error_proveedor_externo():
    mock_estrategia = MagicMock()
    mock_estrategia.generar_respuesta.side_effect = Exception(
        "API Key invalida o cuota agotada"
    )

    mock_agente = MagicMock()
    mock_agente.estrategia = mock_estrategia

    mock_fabrica = MagicMock()
    mock_fabrica.crear_autor.return_value = mock_agente

    servicio = IAService(fabrica_agente=mock_fabrica)

    contexto = {"titulo": "¿Cómo usar pytest?", "cuerpo": "Explica assertions."}
    datos_agente = {"id": 2, "nombre": "Bot-OpenAI", "estrategia": "OpenAI"}

    resultado = servicio.generar_respuesta_automatica(contexto, datos_agente)

    assert "No se pudo completar la respuesta del Agente IA" in resultado
    assert "API Key invalida o cuota agotada" in resultado