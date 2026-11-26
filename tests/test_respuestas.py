import pytest

from plataforma_qa import create_app
from plataforma_qa.config import Config
from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Pregunta, Respuesta, User
from plataforma_qa.services import respuestas as servicio


class ConfigPrueba(Config):
    TESTING = True
    SECRET_KEY = "clave-de-prueba"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


@pytest.fixture
def app():
    app = create_app(ConfigPrueba)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def _usuario(nombre):
    usuario = User(name=nombre, email=f"{nombre.lower()}@example.com", password="x")
    db.session.add(usuario)
    db.session.commit()
    return usuario


def _cliente(app, usuario=None):
    """Cliente HTTP; si se pasa un usuario, ya tiene la sesión iniciada."""
    cliente = app.test_client()
    if usuario is not None:
        with cliente.session_transaction() as sesion:
            sesion["user_id"] = usuario.id
    return cliente


@pytest.fixture
def pregunta(app):
    ana = _usuario("Ana")
    categoria = Categoria(nombre="Python")
    db.session.add(categoria)
    db.session.commit()
    pregunta = Pregunta(
        titulo="¿Qué es Flask?",
        cuerpo="Quiero entenderlo.",
        user_id=ana.id,
        categoria_id=categoria.id,
    )
    db.session.add(pregunta)
    db.session.commit()
    return pregunta


def test_responder_requiere_sesion(app, pregunta):
    respuesta = app.test_client().post(
        f"/preguntas/{pregunta.id}/respuestas", data={"cuerpo": "Hola"}
    )
    assert respuesta.status_code == 302
    assert "/auth/login" in respuesta.headers["Location"]
    assert Respuesta.query.count() == 0


def test_usuario_responde_y_la_respuesta_se_ve_en_el_detalle(app, pregunta):
    beto = _usuario("Beto")
    respuesta = _cliente(app, beto).post(
        f"/preguntas/{pregunta.id}/respuestas",
        data={"cuerpo": "Es un microframework"},
        follow_redirects=True,
    )
    html = respuesta.get_data(as_text=True)
    assert "Es un microframework" in html
    assert "Beto" in html


def test_solo_el_autor_de_la_pregunta_acepta_y_solo_una_a_la_vez(app, pregunta):
    ana = db.session.get(User, pregunta.user_id)
    beto = _usuario("Beto")
    id1 = servicio.crear_respuesta(pregunta, beto, "Primera").id
    id2 = servicio.crear_respuesta(pregunta, beto, "Segunda").id

    # Beto no es el autor de la pregunta: no puede aceptar.
    intento = _cliente(app, beto).post(f"/preguntas/respuestas/{id1}/aceptar")
    assert intento.status_code == 403

    cliente_ana = _cliente(app, ana)
    cliente_ana.post(f"/preguntas/respuestas/{id1}/aceptar")
    cliente_ana.post(f"/preguntas/respuestas/{id2}/aceptar")

    db.session.expire_all()
    assert db.session.get(Respuesta, id1).es_aceptada is False
    assert db.session.get(Respuesta, id2).es_aceptada is True


def test_respuesta_del_agente_ia_no_tiene_autor_y_nadie_la_edita(app, pregunta):
    ia = servicio.crear_respuesta_ia(pregunta, "Respuesta automática", "Asistente IA")
    assert ia.es_ia is True
    assert ia.user_id is None

    ana = db.session.get(User, pregunta.user_id)
    with pytest.raises(PermissionError):
        servicio.modificar_respuesta(ia, ana, "Cambiada")

    html = _cliente(app).get(f"/preguntas/{pregunta.id}").get_data(as_text=True)
    assert "Asistente IA" in html


def test_solo_el_autor_borra_su_respuesta(app, pregunta):
    beto = _usuario("Beto")
    carla = _usuario("Carla")
    respuesta_id = servicio.crear_respuesta(pregunta, beto, "Mía").id
    url = f"/preguntas/respuestas/{respuesta_id}/delete"

    assert _cliente(app, carla).post(url).status_code == 403
    assert Respuesta.query.count() == 1

    assert _cliente(app, beto).post(url).status_code == 302
    assert Respuesta.query.count() == 0


def test_borrar_una_pregunta_borra_sus_respuestas(app, pregunta):
    servicio.crear_respuesta(pregunta, db.session.get(User, pregunta.user_id), "Una")
    db.session.delete(pregunta)
    db.session.commit()
    assert Respuesta.query.count() == 0