import pytest

from plataforma_qa import create_app
from plataforma_qa.config import Config
from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Pregunta, User, Voto
from plataforma_qa.services import respuestas as respuestas_service
from plataforma_qa.services import votos as votos_service


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
    """Cliente HTTP; si se pasa un usuario, ya tiene la sesión iniciada."""
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


# --- Votos --------------------------------------------------------------------


def test_votar_suma_cambia_y_retira_el_voto(app, pregunta):
    beto = _usuario("Beto")
    carla = _usuario("Carla")

    assert votos_service.votar(pregunta, beto, 1) == 1
    assert votos_service.votar(pregunta, carla, 1) == 2
    assert votos_service.votar(pregunta, beto, -1) == 0  # cambia +1 por -1
    assert votos_service.votar(pregunta, beto, -1) == 1  # repetir lo retira
    assert Voto.query.filter_by(user_id=beto.id).count() == 0

    respuesta = respuestas_service.crear_respuesta(pregunta, carla, "Una respuesta")
    assert votos_service.votar(respuesta, beto, 1) == 1  # también en respuestas

    with pytest.raises(ValueError):
        votos_service.votar(pregunta, beto, 5)
    with pytest.raises(PermissionError):
        votos_service.votar(pregunta, None, 1)


def test_web_votar_requiere_sesion_y_suma(app, pregunta):
    pregunta_id = pregunta.id
    url = f"/preguntas/{pregunta_id}/votar"

    sin_sesion = app.test_client().post(url, data={"valor": "1"})
    assert sin_sesion.status_code == 302
    assert "/auth/login" in sin_sesion.headers["Location"]

    _cliente(app, _usuario("Beto")).post(url, data={"valor": "1"})
    db.session.expire_all()
    assert votos_service.puntuacion(db.session.get(Pregunta, pregunta_id)) == 1


# --- API de preguntas ----------------------------------------------------------


def test_api_preguntas_crear_listar_y_leer(app, categoria):
    categoria_id = categoria.id
    ana = _usuario("Ana")
    anonimo = app.test_client()
    datos = {
        "titulo": "¿Qué es WSGI?",
        "cuerpo": "Explicación, por favor.",
        "categoria_id": categoria_id,
        "etiquetas": ["#Flask", "web"],
    }

    assert anonimo.post("/api/preguntas", json=datos).status_code == 401

    respuesta = _cliente(app, ana).post("/api/preguntas", json=datos)
    assert respuesta.status_code == 201
    creada = respuesta.get_json()
    assert respuesta.headers["Location"].endswith(f"/api/preguntas/{creada['id']}")
    assert creada["etiquetas"] == ["flask", "web"]
    assert creada["autor"]["nombre"] == "Ana"
    assert "ana@example.com" not in respuesta.get_data(as_text=True)

    assert anonimo.get("/api/preguntas").get_json()[0]["id"] == creada["id"]
    assert anonimo.get(f"/api/preguntas/{creada['id']}").get_json() == creada
    assert anonimo.get("/api/preguntas/999").status_code == 404


def test_api_preguntas_permisos_y_validaciones(app, pregunta):
    ana = db.session.get(User, pregunta.user_id)
    beto = _usuario("Beto")
    url = f"/api/preguntas/{pregunta.id}"

    assert _cliente(app, beto).patch(url, json={"titulo": "x"}).status_code == 403
    assert _cliente(app, beto).delete(url).status_code == 403

    cliente = _cliente(app, ana)
    assert cliente.patch(url, json={"titulo": "   "}).status_code == 400
    assert cliente.patch(url, json={}).status_code == 400
    sin_categoria = {"titulo": "t", "cuerpo": "c", "categoria_id": 999}
    assert cliente.post("/api/preguntas", json=sin_categoria).status_code == 400

    modificada = cliente.patch(url, json={"titulo": "Nuevo", "etiquetas": []})
    assert modificada.status_code == 200
    assert modificada.get_json()["titulo"] == "Nuevo"

    assert cliente.delete(url).status_code == 204
    assert cliente.get(url).status_code == 404


# --- API de respuestas, votos y categorías -------------------------------------


def test_api_respuestas_crear_y_aceptar(app, pregunta):
    ana = db.session.get(User, pregunta.user_id)
    beto = _usuario("Beto")
    base = f"/api/preguntas/{pregunta.id}/respuestas"

    assert _cliente(app).post(base, json={"cuerpo": "x"}).status_code == 401
    assert _cliente(app, beto).post(base, json={"cuerpo": " "}).status_code == 400

    creada = _cliente(app, beto).post(base, json={"cuerpo": "Mi respuesta"})
    assert creada.status_code == 201
    respuesta_id = creada.get_json()["id"]

    aceptar = f"/api/respuestas/{respuesta_id}/aceptar"
    assert _cliente(app, beto).post(aceptar).status_code == 403  # no es el autor
    aceptada = _cliente(app, ana).post(aceptar)
    assert aceptada.status_code == 200
    assert aceptada.get_json()["es_aceptada"] is True
    assert _cliente(app).get(base).get_json()[0]["es_aceptada"] is True

    assert _cliente(app, beto).delete(f"/api/respuestas/{respuesta_id}").status_code == 204


def test_api_votos(app, pregunta):
    beto = _usuario("Beto")
    cliente = _cliente(app, beto)
    url = f"/api/preguntas/{pregunta.id}/votos"

    assert _cliente(app).post(url, json={"valor": 1}).status_code == 401
    assert cliente.post(url, json={"valor": 1}).get_json() == {"puntuacion": 1}
    assert cliente.post(url, json={"valor": 7}).status_code == 400
    assert cliente.post(url, json={"valor": -1}).get_json() == {"puntuacion": -1}

    respuesta_id = respuestas_service.crear_respuesta(pregunta, beto, "Resp").id
    en_respuesta = cliente.post(f"/api/respuestas/{respuesta_id}/votos", json={"valor": 1})
    assert en_respuesta.get_json() == {"puntuacion": 1}
    assert cliente.post("/api/preguntas/999/votos", json={"valor": 1}).status_code == 404


def test_api_categorias(app, pregunta):
    cliente = _cliente(app, _usuario("Admin", "admin"))  # gestionar categorías: solo admin

    assert _cliente(app).post("/api/categorias", json={"nombre": "Flask"}).status_code == 401
    creada = cliente.post("/api/categorias", json={"nombre": "Flask"})
    assert creada.status_code == 201
    nueva_id = creada.get_json()["id"]

    assert cliente.post("/api/categorias", json={"nombre": "flask"}).status_code == 409
    renombrada = cliente.patch(f"/api/categorias/{nueva_id}", json={"nombre": "Django"})
    assert renombrada.get_json()["nombre"] == "Django"

    nombres = [c["nombre"] for c in _cliente(app).get("/api/categorias").get_json()]
    assert nombres == ["Django", "Python"]

    # La categoría de la pregunta no se puede borrar; la nueva sí.
    assert cliente.delete(f"/api/categorias/{pregunta.categoria_id}").status_code == 409
    assert cliente.delete(f"/api/categorias/{nueva_id}").status_code == 204