"""Reglas de negocio de las preguntas usadas por la API."""

from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Etiqueta, Pregunta
from plataforma_qa.services.permisos import es_admin
from plataforma_qa.services.validacion import (
    MAX_TITULO,
    normalizar_etiquetas,
    texto_obligatorio,
)


def puede_modificar(pregunta, usuario) -> bool:
    """Solo el autor edita su pregunta."""
    return usuario is not None and pregunta.user_id == usuario.id


def puede_borrar(pregunta, usuario) -> bool:
    """El autor borra la suya; el admin puede borrar cualquiera."""
    return es_admin(usuario) or puede_modificar(pregunta, usuario)


def _categoria(categoria_id) -> Categoria:
    if isinstance(categoria_id, bool) or not isinstance(categoria_id, int):
        raise ValueError("El campo 'categoria_id' es obligatorio y debe ser un número.")  # noqa: TRY004
    categoria = db.session.get(Categoria, categoria_id)
    if categoria is None:
        raise ValueError("La categoría indicada no existe.")
    return categoria


def _etiquetas(nombres) -> list[Etiqueta]:
    """Reutiliza las etiquetas que ya existen y crea las que faltan."""
    etiquetas = []
    for nombre in normalizar_etiquetas(nombres):
        existente = db.session.scalar(
            db.select(Etiqueta).where(Etiqueta.nombre == nombre)
        )
        etiquetas.append(existente or Etiqueta(nombre=nombre))
    return etiquetas


def listar_preguntas(categoria_id=None, etiqueta=None) -> list[Pregunta]:
    """Las más nuevas primero. Se puede filtrar por categoría y/o etiqueta."""
    consulta = db.select(Pregunta)
    if categoria_id is not None:
        consulta = consulta.where(Pregunta.categoria_id == categoria_id)
    if etiqueta:
        nombre = etiqueta.strip().lstrip("#").lower()
        consulta = consulta.where(Pregunta.etiquetas.any(Etiqueta.nombre == nombre))
    consulta = consulta.order_by(
        Pregunta.fecha_publicacion.desc(), Pregunta.id.desc()
    )
    return list(db.session.scalars(consulta))


def crear_pregunta(autor, titulo, cuerpo, categoria_id, etiquetas=None) -> Pregunta:
    # Se valida todo antes de tocar la base.
    titulo = texto_obligatorio(titulo, "titulo", MAX_TITULO)
    cuerpo = texto_obligatorio(cuerpo, "cuerpo")
    categoria = _categoria(categoria_id)
    lista_etiquetas = _etiquetas(etiquetas)

    pregunta = Pregunta(
        titulo=titulo, cuerpo=cuerpo, user_id=autor.id, categoria_id=categoria.id
    )
    pregunta.etiquetas = lista_etiquetas
    db.session.add(pregunta)
    db.session.commit()
    return pregunta


def modificar_pregunta(
    pregunta, solicitante, titulo=None, cuerpo=None, categoria_id=None, etiquetas=None
) -> Pregunta:
    """Cambia solo lo que se envía (None = no tocar). etiquetas=[] las borra todas."""
    if not puede_modificar(pregunta, solicitante):
        raise PermissionError("Solo el autor puede modificar la pregunta.")
    if titulo is None and cuerpo is None and categoria_id is None and etiquetas is None:
        raise ValueError("No hay nada para modificar.")

    # Se valida todo antes de asignar, así un error no deja la pregunta a medias.
    nuevo_titulo = None if titulo is None else texto_obligatorio(titulo, "titulo", MAX_TITULO)
    nuevo_cuerpo = None if cuerpo is None else texto_obligatorio(cuerpo, "cuerpo")
    nueva_categoria = None if categoria_id is None else _categoria(categoria_id)
    nuevas_etiquetas = None if etiquetas is None else _etiquetas(etiquetas)

    if nuevo_titulo is not None:
        pregunta.titulo = nuevo_titulo
    if nuevo_cuerpo is not None:
        pregunta.cuerpo = nuevo_cuerpo
    if nueva_categoria is not None:
        pregunta.categoria_id = nueva_categoria.id
    if nuevas_etiquetas is not None:
        pregunta.etiquetas = nuevas_etiquetas
    db.session.commit()
    return pregunta


def borrar_pregunta(pregunta, solicitante) -> None:
    if not puede_borrar(pregunta, solicitante):
        raise PermissionError("Solo el autor o un administrador pueden borrar la pregunta.")
    db.session.delete(pregunta)
    db.session.commit()