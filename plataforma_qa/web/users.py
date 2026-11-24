from flask import Blueprint, redirect, render_template, request, url_for

from plataforma_qa.extensions import db
from plataforma_qa.models.user import User

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/")
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("users/index.html", users=users)


@users_bp.post("/")
def create_user():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()

    if name and email:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()

    return redirect(url_for("users.list_users"))
