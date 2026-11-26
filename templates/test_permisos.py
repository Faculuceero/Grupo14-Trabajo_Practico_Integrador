import pytest

from plataforma_qa import create_app
from plataforma_qa.config import Config
from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Pregunta, User
from plataforma_qa.services import respuestas as respuestas_service


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


def _usuario(nombre, rol="usuario"):
    usuario = User(
        name=nombre, email=f"{nombre.lower()}@example.com", password="x", rol=rol
    )
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


@pytest.fixture
def pregunta(app, categoria):
    ana = _usuario("Ana")
    pregunta = Pregunta(
        titulo="¿Qué es Flask?",
        cuerpo="Quiero entenderlo.",
        user_id=ana.id,
        categoria_id=categoria.id,
    )
    db.session.add(pregunta)
    db.session.commit()
    return pregunta


def test_api_aceptar_editar_y_borrar_segun_el_rol(app, pregunta):
    ana = db.session.get(User, pregunta.user_id)
    beto = _usuario("Beto")
    admin = _usuario("Admin", "admin")
    respuesta_id = respuestas_service.crear_respuesta(pregunta, beto, "Respuesta").id
    url_respuesta = f"/api/respuestas/{respuesta_id}"
    url_pregunta = f"/api/preguntas/{pregunta.id}"

    # Aceptar: solo el autor de la pregunta (ni otro usuario ni el admin).
    aceptar = f"{url_respuesta}/aceptar"
    assert _cliente(app, beto).post(aceptar).status_code == 403
    assert _cliente(app, admin).post(aceptar).status_code == 403
    assert _cliente(app, ana).post(aceptar).status_code == 200

    # Un usuario común no toca lo ajeno.
    assert _cliente(app, ana).delete(url_respuesta).status_code == 403
    assert _cliente(app, beto).delete(url_pregunta).status_code == 403

    # El admin no edita lo ajeno, pero sí lo borra.
    assert _cliente(app, admin).patch(url_respuesta, json={"cuerpo": "x"}).status_code == 403
    assert _cliente(app, admin).patch(url_pregunta, json={"titulo": "x"}).status_code == 403
    assert _cliente(app, admin).delete(url_respuesta).status_code == 204
    assert _cliente(app, admin).delete(url_pregunta).status_code == 204


def test_api_solo_el_admin_gestiona_categorias(app, categoria):
    url = f"/api/categorias/{categoria.id}"
    comun = _cliente(app, _usuario("Beto"))
    assert comun.post("/api/categorias", json={"nombre": "Flask"}).status_code == 403
    assert comun.patch(url, json={"nombre": "Otra"}).status_code == 403
    assert comun.delete(url).status_code == 403

    admin = _cliente(app, _usuario("Admin", "admin"))
    creada = admin.post("/api/categorias", json={"nombre": "Flask"})
    assert creada.status_code == 201
    assert admin.patch(url, json={"nombre": "Otra"}).status_code == 200
    assert admin.delete(f"/api/categorias/{creada.get_json()['id']}").status_code == 204


def test_web_permisos_de_preguntas_y_categorias(app, pregunta):
    url = f"/preguntas/{pregunta.id}"
    beto = _usuario("Beto")
    admin = _usuario("Admin", "admin")

    assert _cliente(app).post(f"{url}/delete").status_code == 302  # al login

    comun = _cliente(app, beto)
    assert comun.get(f"{url}/edit").status_code == 403
    assert comun.post(f"{url}/delete").status_code == 403
    assert comun.post("/preguntas/categorias", data={"nombre": "Nueva"}).status_code == 403
    pagina = comun.get(url).get_data(as_text=True)
    assert "Editar pregunta" not in pagina
    assert "Eliminar pregunta" not in pagina

    moderador = _cliente(app, admin)
    pagina = moderador.get(url).get_data(as_text=True)
    assert "Eliminar pregunta" in pagina
    assert "Editar pregunta" not in pagina  # el admin borra, pero no edita lo ajeno
    assert moderador.post("/preguntas/categorias", data={"nombre": "Nueva"}).status_code == 302
    assert moderador.post(f"{url}/delete").status_code == 302
    assert _cliente(app).get(url).status_code == 404