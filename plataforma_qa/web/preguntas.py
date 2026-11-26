from flask import (
    Blueprint,
    abort,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
)

from plataforma_qa.extensions import db
from plataforma_qa.models import Categoria, Etiqueta, Pregunta, Respuesta, User
from plataforma_qa.services import respuestas as respuestas_service
from plataforma_qa.services import votos as votos_service
from plataforma_qa.web.acceso import login_required

preguntas_bp = Blueprint("preguntas", __name__, url_prefix="/preguntas")


def _obtener_autor_actual() -> User | None:
    if getattr(g, "user", None) is not None:
        return g.user
    return User.query.order_by(User.id.asc()).first()


def _procesar_etiquetas(etiquetas_ids: list[str], nuevas_etiquetas: str) -> list[Etiqueta]:
    seleccionadas: list[Etiqueta] = []

    for eid in etiquetas_ids:
        if eid.isdigit():
            etiqueta = db.session.get(Etiqueta, int(eid))
            if etiqueta and etiqueta not in seleccionadas:
                seleccionadas.append(etiqueta)

    for raw in nuevas_etiquetas.split(","):
        nombre = raw.strip().lower()
        if not nombre:
            continue
        etiqueta = Etiqueta.query.filter_by(nombre=nombre).first()
        if not etiqueta:
            etiqueta = Etiqueta(nombre=nombre)
            db.session.add(etiqueta)
        if etiqueta not in seleccionadas:
            seleccionadas.append(etiqueta)

    return seleccionadas


@preguntas_bp.get("/")
def list_preguntas():
    preguntas = Pregunta.query.order_by(Pregunta.fecha_publicacion.desc()).all()
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    return render_template(
        "preguntas/index.html",
        preguntas=preguntas,
        categorias=categorias,
    )


@preguntas_bp.post("/categorias")
def create_categoria():
    nombre = request.form.get("nombre", "").strip()
    if not nombre:
        flash("El nombre de la categoría no puede estar vacío.", "error")
        return redirect(url_for("preguntas.list_preguntas"))

    existente = Categoria.query.filter_by(nombre=nombre).first()
    if existente:
        flash("Esa categoría ya existe.", "error")
        return redirect(url_for("preguntas.list_preguntas"))

    db.session.add(Categoria(nombre=nombre))
    db.session.commit()
    flash(f"Categoría '{nombre}' creada.", "success")
    return redirect(url_for("preguntas.list_preguntas"))


@preguntas_bp.route("/nueva", methods=["GET", "POST"])
def create_pregunta():
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    etiquetas = Etiqueta.query.order_by(Etiqueta.nombre.asc()).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        cuerpo = request.form.get("cuerpo", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        nueva_categoria = request.form.get("nueva_categoria", "").strip()
        etiquetas_ids = request.form.getlist("etiquetas")
        nuevas_etiquetas = request.form.get("nuevas_etiquetas", "")

        autor = _obtener_autor_actual()
        if autor is None:
            flash("Debe existir al menos un usuario registrado para publicar.", "error")
            return redirect(url_for("users.list_users"))

        if not titulo or not cuerpo:
            flash("El título y el cuerpo de la pregunta son obligatorios.", "error")
            return render_template(
                "preguntas/new.html",
                categorias=categorias,
                etiquetas=etiquetas,
            )

        categoria = None
        if nueva_categoria:
            categoria = Categoria.query.filter_by(nombre=nueva_categoria).first()
            if not categoria:
                categoria = Categoria(nombre=nueva_categoria)
                db.session.add(categoria)
                db.session.flush()
        elif categoria_id.isdigit():
            categoria = db.session.get(Categoria, int(categoria_id))

        if categoria is None:
            flash("Seleccioná una categoría o creá una nueva.", "error")
            return render_template(
                "preguntas/new.html",
                categorias=categorias,
                etiquetas=etiquetas,
            )

        pregunta = Pregunta(
            titulo=titulo,
            cuerpo=cuerpo,
            user_id=autor.id,
            categoria_id=categoria.id,
        )
        pregunta.etiquetas = _procesar_etiquetas(etiquetas_ids, nuevas_etiquetas)

        db.session.add(pregunta)
        db.session.commit()
        flash("Pregunta publicada correctamente.", "success")
        return redirect(url_for("preguntas.detail_pregunta", pregunta_id=pregunta.id))

    return render_template(
        "preguntas/new.html",
        categorias=categorias,
        etiquetas=etiquetas,
    )


@preguntas_bp.get("/<int:pregunta_id>")
def detail_pregunta(pregunta_id: int):
    pregunta = db.get_or_404(Pregunta, pregunta_id)
    # La aceptada primero; después, de la más vieja a la más nueva.
    respuestas = sorted(
        pregunta.respuestas,
        key=lambda r: (not r.es_aceptada, r.fecha_publicacion),
    )
    return render_template(
        "preguntas/detail.html",
        pregunta=pregunta,
        respuestas=respuestas,
        puede_aceptar=respuestas_service.puede_aceptar,
        puede_modificar=respuestas_service.puede_modificar,
        puntuacion=votos_service.puntuacion,
    )


@preguntas_bp.route("/<int:pregunta_id>/edit", methods=["GET", "POST"])
def edit_pregunta(pregunta_id: int):
    pregunta = db.get_or_404(Pregunta, pregunta_id)
    categorias = Categoria.query.order_by(Categoria.nombre.asc()).all()
    etiquetas = Etiqueta.query.order_by(Etiqueta.nombre.asc()).all()

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        cuerpo = request.form.get("cuerpo", "").strip()
        categoria_id = request.form.get("categoria_id", "").strip()
        etiquetas_ids = request.form.getlist("etiquetas")
        nuevas_etiquetas = request.form.get("nuevas_etiquetas", "")

        if not titulo or not cuerpo or not categoria_id.isdigit():
            flash("Completá título, cuerpo y categoría.", "error")
            return render_template(
                "preguntas/edit.html",
                pregunta=pregunta,
                categorias=categorias,
                etiquetas=etiquetas,
            )

        categoria = db.session.get(Categoria, int(categoria_id))
        if categoria is None:
            flash("La categoría seleccionada no existe.", "error")
            return render_template(
                "preguntas/edit.html",
                pregunta=pregunta,
                categorias=categorias,
                etiquetas=etiquetas,
            )

        pregunta.titulo = titulo
        pregunta.cuerpo = cuerpo
        pregunta.categoria_id = categoria.id
        pregunta.etiquetas = _procesar_etiquetas(etiquetas_ids, nuevas_etiquetas)

        db.session.commit()
        flash("Pregunta actualizada correctamente.", "success")
        return redirect(url_for("preguntas.detail_pregunta", pregunta_id=pregunta.id))

    return render_template(
        "preguntas/edit.html",
        pregunta=pregunta,
        categorias=categorias,
        etiquetas=etiquetas,
    )


@preguntas_bp.post("/<int:pregunta_id>/delete")
def delete_pregunta(pregunta_id: int):
    pregunta = db.get_or_404(Pregunta, pregunta_id)
    db.session.delete(pregunta)
    db.session.commit()
    flash("Pregunta eliminada.", "success")
    return redirect(url_for("preguntas.list_preguntas"))

# --- Respuestas ---------------------------------------------------------------


@preguntas_bp.post("/<int:pregunta_id>/respuestas")
@login_required
def create_respuesta(pregunta_id: int):
    pregunta = db.get_or_404(Pregunta, pregunta_id)
    try:
        respuestas_service.crear_respuesta(
            pregunta, g.user, request.form.get("cuerpo")
        )
        flash("Respuesta publicada.", "success")
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("preguntas.detail_pregunta", pregunta_id=pregunta.id))


@preguntas_bp.route("/respuestas/<int:respuesta_id>/edit", methods=["GET", "POST"])
@login_required
def edit_respuesta(respuesta_id: int):
    respuesta = db.get_or_404(Respuesta, respuesta_id)
    if not respuestas_service.puede_modificar(respuesta, g.user):
        abort(403)

    if request.method == "POST":
        try:
            respuestas_service.modificar_respuesta(
                respuesta, g.user, request.form.get("cuerpo")
            )
        except ValueError as error:
            flash(str(error), "error")
            return render_template(
                "preguntas/edit_respuesta.html", respuesta=respuesta
            ), 400
        flash("Respuesta actualizada.", "success")
        return redirect(
            url_for("preguntas.detail_pregunta", pregunta_id=respuesta.pregunta_id)
        )

    return render_template("preguntas/edit_respuesta.html", respuesta=respuesta)


@preguntas_bp.post("/respuestas/<int:respuesta_id>/delete")
@login_required
def delete_respuesta(respuesta_id: int):
    respuesta = db.get_or_404(Respuesta, respuesta_id)
    pregunta_id = respuesta.pregunta_id
    try:
        respuestas_service.borrar_respuesta(respuesta, g.user)
    except PermissionError:
        abort(403)
    flash("Respuesta eliminada.", "success")
    return redirect(url_for("preguntas.detail_pregunta", pregunta_id=pregunta_id))


@preguntas_bp.post("/respuestas/<int:respuesta_id>/aceptar")
@login_required
def accept_respuesta(respuesta_id: int):
    respuesta = db.get_or_404(Respuesta, respuesta_id)
    try:
        respuestas_service.aceptar_respuesta(respuesta, g.user)
    except PermissionError:
        abort(403)
    flash("Respuesta marcada como aceptada.", "success")
    return redirect(
        url_for("preguntas.detail_pregunta", pregunta_id=respuesta.pregunta_id)
    )

# --- Votos --------------------------------------------------------------------


def _votar_y_volver(publicacion, pregunta_id: int):
    try:
        votos_service.votar(publicacion, g.user, request.form.get("valor", type=int))
    except ValueError as error:
        flash(str(error), "error")
    return redirect(url_for("preguntas.detail_pregunta", pregunta_id=pregunta_id))


@preguntas_bp.post("/<int:pregunta_id>/votar")
@login_required
def votar_pregunta(pregunta_id: int):
    pregunta = db.get_or_404(Pregunta, pregunta_id)
    return _votar_y_volver(pregunta, pregunta.id)


@preguntas_bp.post("/respuestas/<int:respuesta_id>/votar")
@login_required
def votar_respuesta(respuesta_id: int):
    respuesta = db.get_or_404(Respuesta, respuesta_id)
    return _votar_y_volver(respuesta, respuesta.pregunta_id)