"""Piezas compartidas por los blueprints de la API JSON."""

from functools import wraps

from flask import g, jsonify, request

from plataforma_qa.extensions import db
from plataforma_qa.services.errores import Conflicto, NoEncontrado


def error(mensaje, codigo):
    return jsonify({"error": mensaje}), codigo


def login_required_api(vista):
    """Responde 401 en JSON si no hay sesión (el login web guarda g.user)."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if g.get("user") is None:
            return error("Hace falta iniciar sesión.", 401)
        return vista(*args, **kwargs)

    return envoltura


def datos_json() -> dict:
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
            raise ValueError("El pedido debe ser un objeto JSON.")  # noqa: TRY004
    return datos


def obtener_o_404(modelo, objeto_id, nombre):
    objeto = db.session.get(modelo, objeto_id)
    if objeto is None:
        raise NoEncontrado(f"No existe {nombre} {objeto_id}.")
    return objeto


def manejar_errores(blueprint):
    """Convierte las excepciones del servicio en respuestas JSON con su código."""

    @blueprint.errorhandler(ValueError)
    def _datos_invalidos(excepcion):
        return error(str(excepcion), 400)

    @blueprint.errorhandler(PermissionError)
    def _sin_permiso(excepcion):
        return error(str(excepcion), 403)

    @blueprint.errorhandler(NoEncontrado)
    def _no_encontrado(excepcion):
        return error(str(excepcion), 404)

    @blueprint.errorhandler(Conflicto)
    def _conflicto(excepcion):
        return error(str(excepcion), 409)