"""Pruebas de AgenteIA, contexto del patrón Strategy (responsable: Facu Lucero)."""

from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from plataforma_qa import create_app
from plataforma_qa.config import Config
from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM
from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Etiqueta, Pregunta, Respuesta, User
from plataforma_qa.services import agente_ia
from plataforma_qa.services.errores import AgenteIAError, Conflicto


class ConfigPrueba(Config):
    TESTING = True
    SECRET_KEY = "clave-de-prueba"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class EstrategiaPrueba(EstrategiaLLM):
    """Proveedor de IA falso: no usa red."""

    def __init__(self, texto="Respuesta de la IA", falla=False):
        self.texto = texto
        self.falla = falla
        self.prompts = []

    def generar_texto(self, prompt):
        self.prompts.append(prompt)
        if self.falla:
            raise RuntimeError("proveedor caído")
        return self.texto


@pytest.fixture
def app():
    app = create_app(ConfigPrueba)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def con_ia(monkeypatch):
    """Hace que web, API y comando usen un proveedor de IA falso."""
    monkeypatch.delenv("IA_AGENTE_NOMBRE", raising=False)
    estrategia = EstrategiaPrueba()
    monkeypatch.setattr(agente_ia, "crear_estrategia", lambda proveedor=None: estrategia)
    return estrategia


def _usuario(nombre):
    usuario = User(name=nombre, email=f"{nombre.lower()}@example.com", password="x")
    db.session.add(usuario)
    db.session.commit()
    return usuario


def _cliente(app, usuario=None):
    cliente = app.test_client()
    if usuario is not None:
        with cliente.session_transaction() as sesion:
            sesion["user_id"] = usuario.id
    return cliente


@pytest.fixture
def categoria(app):
    categoria = Categoria(nombre="Python")
    db.session.add(categoria)
    db.session.commit()
    return categoria


def _pregunta(autor, categoria, titulo="¿Qué es Flask?", minutos=0, etiquetas=()):
    pregunta = Pregunta(
        titulo=titulo,
        cuerpo="Quiero entenderlo.",
        user_id=autor.id,
        categoria_id=categoria.id,
        fecha_publicacion=datetime.now(UTC) - timedelta(minutes=minutos),
    )
    pregunta.etiquetas = [Etiqueta(nombre=n) for n in etiquetas]
    db.session.add(pregunta)
    db.session.commit()
    return pregunta


# --- Reglas del agente ---------------------------------------------------------


def test_debe_responder_segun_etiqueta_tiempo_y_respuestas():
    ahora = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)

    def pregunta(minutos, etiquetas=(), respuestas=()):
        return SimpleNamespace(
            fecha_publicacion=ahora - timedelta(minutes=minutos),
            etiquetas=[SimpleNamespace(nombre=n) for n in etiquetas],
            respuestas=list(respuestas),
        )

    assert agente_ia.debe_responder(pregunta(0, ["ia-help"]), 30, ahora)
    assert agente_ia.debe_responder(pregunta(0, ["#IA-Help"]), 30, ahora)
    assert agente_ia.debe_responder(pregunta(31), 30, ahora)
    assert not agente_ia.debe_responder(pregunta(5), 30, ahora)
    assert not agente_ia.debe_responder(pregunta(60, ["ia-help"], [object()]), 30, ahora)


def test_responder_con_ia_guarda_la_respuesta_y_si_falla_no_guarda_nada(app, categoria):
    ana = _usuario("Ana")
    pregunta = _pregunta(ana, categoria)

    estrategia = EstrategiaPrueba("La IA responde")
    respuesta = agente_ia.responder_con_ia(pregunta, estrategia=estrategia)
    assert respuesta.es_ia is True
    assert respuesta.user_id is None
    assert respuesta.cuerpo == "La IA responde"
    assert respuesta.nombre_autor == "Asistente IA"
    assert "¿Qué es Flask?" in estrategia.prompts[0]
    with pytest.raises(Conflicto):  # ya tiene una respuesta: no responde dos veces
        agente_ia.responder_con_ia(pregunta, estrategia=estrategia)

    otra = _pregunta(ana, categoria, titulo="Otra pregunta")
    with pytest.raises(AgenteIAError, match="proveedor caído"):
        agente_ia.responder_con_ia(otra, estrategia=EstrategiaPrueba(falla=True))
    assert Respuesta.query.filter_by(pregunta_id=otra.id).count() == 0


def test_responder_pendientes_responde_solo_las_que_corresponden(app, categoria):
    ana = _usuario("Ana")
    vieja = _pregunta(ana, categoria, "Vieja sin responder", minutos=40)
    _pregunta(ana, categoria, "Nueva sin etiqueta", minutos=0)
    con_etiqueta = _pregunta(ana, categoria, "Con etiqueta", etiquetas=["ia-help"])
    ya_respondida = _pregunta(ana, categoria, "Vieja respondida", minutos=90)
    db.session.add(Respuesta(pregunta_id=ya_respondida.id, user_id=ana.id, cuerpo="Hola"))
    db.session.commit()
    ids_esperados = {vieja.id, con_etiqueta.id}

    respondidas, fallidas = agente_ia.responder_pendientes(30, EstrategiaPrueba())

    assert {r.pregunta_id for r in respondidas} == ids_esperados
    assert fallidas == []


def test_comando_responder_pendientes(app, categoria, con_ia):
    _pregunta(_usuario("Ana"), categoria, minutos=40)

    resultado = app.test_cli_runner().invoke(args=["responder-pendientes", "--minutos", "30"])

    assert resultado.exit_code == 0
    assert "respondidas por el agente IA: 1" in resultado.output


# --- Web -----------------------------------------------------------------------


def test_web_la_etiqueta_ia_help_dispara_la_respuesta_y_el_boton_responde(
    app, categoria, con_ia
):
    ana = _usuario("Ana")
    cliente = _cliente(app, ana)

    creada = cliente.post(
        "/preguntas/nueva",
        data={
            "titulo": "Necesito ayuda",
            "cuerpo": "No entiendo las listas",
            "categoria_id": str(categoria.id),
            "nuevas_etiquetas": "ia-help",
        },
        follow_redirects=True,
    )
    assert "Asistente IA" in creada.get_data(as_text=True)

    sin_etiqueta = _pregunta(ana, categoria, "Sin etiqueta")
    cliente.post(f"/preguntas/{sin_etiqueta.id}/responder-ia")
    assert Respuesta.query.filter_by(pregunta_id=sin_etiqueta.id, es_ia=True).count() == 1


# --- API: auth, usuarios e IA --------------------------------------------------


def test_api_auth_y_usuarios(app):
    cliente = app.test_client()
    registro = {
        "name": "Ana",
        "email": "Ana@Example.com",
        "password": "clave-larga-123",
        "rol": "admin",  # un registro público no puede elegir su rol
    }

    creado = cliente.post("/api/auth/register", json=registro)
    assert creado.status_code == 201
    datos = creado.get_json()
    assert datos["email"] == "ana@example.com"
    assert datos["rol"] == "usuario"
    assert "password" not in creado.get_data(as_text=True)

    assert cliente.get("/api/auth/me").get_json()["name"] == "Ana"
    assert cliente.post("/api/auth/logout").status_code == 204
    assert cliente.get("/api/auth/me").status_code == 401

    mala = {"email": "ana@example.com", "password": "incorrecta"}
    assert cliente.post("/api/auth/login", json=mala).status_code == 401
    buena = {"email": "ana@example.com", "password": "clave-larga-123"}
    assert cliente.post("/api/auth/login", json=buena).status_code == 200
    assert cliente.post("/api/auth/register", json=registro).status_code == 409
    corta = {"name": "X", "email": "x@example.com", "password": "corta"}
    assert cliente.post("/api/auth/register", json=corta).status_code == 400

    publica = app.test_client().get("/api/users").get_json()
    assert publica == [{"id": datos["id"], "name": "Ana", "rol": "usuario"}]

    url = f"/api/users/{datos['id']}"
    assert cliente.patch(url, json={"name": "Ana María"}).get_json()["name"] == "Ana María"
    ajeno = _cliente(app, _usuario("Beto"))
    assert ajeno.patch(url, json={"name": "x"}).status_code == 403


def test_api_respuesta_ia(app, categoria, con_ia):
    ana = _usuario("Ana")
    pregunta = _pregunta(ana, categoria)
    otra = _pregunta(ana, categoria, "Otra pregunta")
    url = f"/api/preguntas/{pregunta.id}/respuesta-ia"
    cliente = _cliente(app, _usuario("Beto"))

    assert app.test_client().post(url).status_code == 401

    creada = cliente.post(url)
    assert creada.status_code == 201
    datos = creada.get_json()
    assert datos["es_ia"] is True
    assert datos["autor"] is None
    assert datos["cuerpo"] == con_ia.texto
    assert cliente.post(url).status_code == 409  # ya tiene respuesta

    con_ia.falla = True
    fallo = cliente.post(f"/api/preguntas/{otra.id}/respuesta-ia")
    assert fallo.status_code == 502
    assert "proveedor caído" in fallo.get_json()["error"]