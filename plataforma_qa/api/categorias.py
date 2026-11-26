"""API JSON de categorías: /api/categorias

    GET    /api/categorias          lista                    público
    GET    /api/categorias/<id>     detalle                  público
    POST   /api/categorias          crear                    requiere sesión
    PATCH  /api/categorias/<id>     renombrar                requiere sesión
    DELETE /api/categorias/<id>     borrar (si no tiene preguntas)   requiere sesión
"""

from flask import Blueprint, jsonify, url_for

from plataforma_qa.api.comun import (
    datos_json,
    login_required_api,
    manejar_errores,
    obtener_o_404,
)
from plataforma_qa.models import Categoria
from plataforma_qa.services import categorias as servicio

categorias_api_bp = Blueprint("categorias_api", __name__, url_prefix="/api/categorias")
manejar_errores(categorias_api_bp)


def a_dict(categoria):
    return {"id": categoria.id, "nombre": categoria.nombre}


@categorias_api_bp.get("")
def listar():
    return jsonify([a_dict(c) for c in servicio.listar_categorias()])


@categorias_api_bp.get("/<int:categoria_id>")
def detalle(categoria_id):
    return jsonify(a_dict(obtener_o_404(Categoria, categoria_id, "la categoría")))


@categorias_api_bp.post("")
@login_required_api
def crear():
    categoria = servicio.crear_categoria(datos_json().get("nombre"))
    respuesta = jsonify(a_dict(categoria))
    respuesta.status_code = 201
    respuesta.headers["Location"] = url_for(
        "categorias_api.detalle", categoria_id=categoria.id
    )
    return respuesta


@categorias_api_bp.patch("/<int:categoria_id>")
@login_required_api
def modificar(categoria_id):
    categoria = obtener_o_404(Categoria, categoria_id, "la categoría")
    servicio.modificar_categoria(categoria, datos_json().get("nombre"))
    return jsonify(a_dict(categoria))


@categorias_api_bp.delete("/<int:categoria_id>")
@login_required_api
def borrar(categoria_id):
    servicio.borrar_categoria(obtener_o_404(Categoria, categoria_id, "la categoría"))
    return "", 204