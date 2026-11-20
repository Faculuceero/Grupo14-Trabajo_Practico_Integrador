"""Pruebas de AgenteIA, contexto del patrón Strategy (responsable: Facu Lucero)."""
from datetime import datetime

import pytest

from plataforma_qa.publicaciones.pregunta import Pregunta
from plataforma_qa.publicaciones.respuesta import Respuesta
from tests.utils import EstrategiaFalsa, EstrategiaFallida, hace_minutos


def test_set_estrategia_cambia_la_estrategia(agente):
    nueva = EstrategiaFalsa("otra")
    agente.set_estrategia(nueva)
    assert agente._estrategia is nueva


def test_generar_respuesta_crea_una_respuesta_del_agente(agente, pregunta):
    r = agente.generar_respuesta(pregunta)
    assert isinstance(r, Respuesta)
    assert r._autor is agente
    assert r._cuerpo.contenido == "respuesta falsa"
    assert r in pregunta._respuestas


def test_el_prompt_incluye_titulo_cuerpo_y_etiquetas(agente, estrategia, pregunta_ia):
    agente.generar_respuesta(pregunta_ia)
    prompt = estrategia.prompts[0]
    assert pregunta_ia._titulo in prompt
    assert pregunta_ia._cuerpo.contenido in prompt
    assert "ia-help" in prompt


def test_si_la_estrategia_falla_no_se_crea_una_respuesta(agente, pregunta):
    agente.set_estrategia(EstrategiaFallida())
    with pytest.raises(RuntimeError) as info:
        agente.generar_respuesta(pregunta)
    assert not isinstance(info.value, NotImplementedError)
    assert pregunta._respuestas == []


def test_debe_responder_si_la_pregunta_tiene_la_etiqueta(agente, pregunta_ia):
    assert agente.debe_responder(pregunta_ia) is True


def test_debe_responder_si_lleva_mucho_tiempo_sin_respuestas(agente, usuario, categoria, texto):
    p = Pregunta("Antigua", texto, hace_minutos(60), usuario, categoria)
    assert agente.debe_responder(p) is True


def test_no_debe_responder_si_es_reciente_y_no_tiene_la_etiqueta(agente, pregunta):
    assert agente.debe_responder(pregunta) is False


def test_no_responde_dos_veces_la_misma_pregunta(agente, pregunta_ia):
    agente.generar_respuesta(pregunta_ia)
    assert agente.debe_responder(pregunta_ia) is False
