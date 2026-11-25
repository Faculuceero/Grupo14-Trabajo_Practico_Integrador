from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from plataforma_qa.extensions import db
from plataforma_qa.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        rol = request.form.get("rol", "usuario")

        if not name or not email or not password:
            flash("Todos los campos son obligatorios.", "error")
            return render_template("auth/register.html"), 400

        existente = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if existente:
            flash("Ya existe un usuario registrado con ese correo.", "error")
            return render_template("auth/register.html"), 400

        nuevo_usuario = User(name=name, email=email, password=password, rol=rol)
        db.session.add(nuevo_usuario)
        db.session.commit()

        session.clear()
        session["user_id"] = nuevo_usuario.id
        return redirect(url_for("users.index"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
        if user is None or user.password != password:
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("auth/login.html"), 401

        session.clear()
        session["user_id"] = user.id
        return redirect(url_for("users.index"))

    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))