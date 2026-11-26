"""API JSON de usuarios. El registro se hace en /api/auth/register.

    GET   /api/users        lista (datos públicos)      público
    GET   /api/users/<id>   detalle (datos públicos)    público
    PATCH /api/users/<id>   cambiar el propio nombre    requiere sesión
"""

from flask import Blueprint, g, jsonify

from plataforma_qa.api.comun import (
    datos_json,
    login_required_api,
    manejar_errores,
    obtener_o_404,
)
from plataforma_qa.models import User
from plataforma_qa.services import usuarios as servicio

users_api_bp = Blueprint("users_api", __name__, url_prefix="/api/users")
manejar_errores(users_api_bp)


def _publico(usuario):
    """Datos públicos: nunca el email ni la contraseña."""
    return {"id": usuario.id, "name": usuario.name, "rol": usuario.rol}


@users_api_bp.get("")
def listar():
    return jsonify([_publico(u) for u in servicio.listar_usuarios()])


@users_api_bp.get("/<int:usuario_id>")
def detalle(usuario_id):
    usuario = obtener_o_404(User, usuario_id, "el usuario")
    datos = _publico(usuario)
    datos["cantidad_preguntas"] = len(usuario.preguntas)
    return jsonify(datos)


@users_api_bp.patch("/<int:usuario_id>")
@login_required_api
def modificar(usuario_id):
    usuario = obtener_o_404(User, usuario_id, "el usuario")
    servicio.modificar_nombre(usuario, g.user, datos_json().get("name"))
    return jsonify(_publico(usuario))