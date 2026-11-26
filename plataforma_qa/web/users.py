from flask import Blueprint, redirect, render_template, request, url_for

from plataforma_qa.extensions import db
from plataforma_qa.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form.get("name") or request.form.get("nombre")
        email = request.form.get("email")

        # Instanciamos el usuario usando la columna 'name' de SQLAlchemy
        nuevo_usuario = User(name=nombre, email=email)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return redirect(url_for("users.index"))

    usuarios = User.query.all() if hasattr(User, "query") else []
    return render_template("users/index.html", usuarios=usuarios)


@users_bp.route("/<int:user_id>")
def detail(user_id: int):
    usuario = User.query.get_or_404(user_id) if hasattr(User, "query") else None
    return render_template("users/detail.html", usuario=usuario, user_id=user_id)