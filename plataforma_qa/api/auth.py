"""API JSON de autenticación (usa la misma sesión que el login web).

    POST /api/auth/register   {"name", "email", "password"}   crea el usuario y abre sesión
    POST /api/auth/login      {"email", "password"}           abre sesión
    POST /api/auth/logout                                     cierra sesión
    GET  /api/auth/me                                         usuario de la sesión (requiere sesión)
"""

from flask import Blueprint, g, jsonify, session, url_for

from plataforma_qa.api.comun import (
    datos_json,
    error,
    login_required_api,
    manejar_errores,
)
from plataforma_qa.services import usuarios as servicio

auth_api_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")
manejar_errores(auth_api_bp)


def _propio(usuario):
    """El usuario ve su propio email; la contraseña no se expone nunca."""
    return {
        "id": usuario.id,
        "name": usuario.name,
        "email": usuario.email,
        "rol": usuario.rol,
    }


def _abrir_sesion(usuario):
    session.clear()  # evita reutilizar una sesión anterior
    session["user_id"] = usuario.id


@auth_api_bp.post("/register")
def registrar():
    datos = datos_json()
    usuario = servicio.crear_usuario(
        datos.get("name"), datos.get("email"), datos.get("password")
    )
    _abrir_sesion(usuario)
    respuesta = jsonify(_propio(usuario))
    respuesta.status_code = 201
    respuesta.headers["Location"] = url_for("users_api.detalle", usuario_id=usuario.id)
    return respuesta


@auth_api_bp.post("/login")
def iniciar_sesion():
    datos = datos_json()
    usuario = servicio.autenticar(datos.get("email"), datos.get("password"))
    if usuario is None:
        return error("Correo o contraseña incorrectos.", 401)
    _abrir_sesion(usuario)
    return jsonify(_propio(usuario))


@auth_api_bp.post("/logout")
def cerrar_sesion():
    session.clear()
    return "", 204


@auth_api_bp.get("/me")
@login_required_api
def yo():
    return jsonify(_propio(g.user))