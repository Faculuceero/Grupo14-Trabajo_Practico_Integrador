from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria
from plataforma_qa.services.errores import Conflicto
from plataforma_qa.services.permisos import exigir_admin
from plataforma_qa.services.validacion import MAX_CATEGORIA, texto_obligatorio


def _por_nombre(nombre):
    return db.session.scalar(
        db.select(Categoria).where(db.func.lower(Categoria.nombre) == nombre.lower())
    )


def listar_categorias():
    return list(db.session.scalars(db.select(Categoria).order_by(Categoria.nombre)))


def crear_categoria(solicitante, nombre) -> Categoria:
    exigir_admin(solicitante, "crear categorías")
    nombre = texto_obligatorio(nombre, "nombre", MAX_CATEGORIA)
    if _por_nombre(nombre) is not None:
        raise Conflicto("Ya existe una categoría con ese nombre.")
    categoria = Categoria(nombre=nombre)
    db.session.add(categoria)
    db.session.commit()
    return categoria


def modificar_categoria(solicitante, categoria, nombre) -> Categoria:
    exigir_admin(solicitante, "modificar categorías")
    nombre = texto_obligatorio(nombre, "nombre", MAX_CATEGORIA)
    otra = _por_nombre(nombre)
    if otra is not None and otra.id != categoria.id:
        raise Conflicto("Ya existe una categoría con ese nombre.")
    categoria.nombre = nombre
    db.session.commit()
    return categoria


def borrar_categoria(solicitante, categoria) -> None:
    exigir_admin(solicitante, "borrar categorías")
    if categoria.preguntas:
        raise Conflicto("No se puede borrar una categoría que tiene preguntas.")
    db.session.delete(categoria)
    db.session.commit()