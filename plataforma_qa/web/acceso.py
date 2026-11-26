from functools import wraps

from flask import flash, g, redirect, url_for


def login_required(vista):
    """Si no hay sesión iniciada, manda al login en vez de ejecutar la vista."""

    @wraps(vista)
    def envoltura(*args, **kwargs):
        if g.get("user") is None:
            flash("Tenés que iniciar sesión para hacer eso.", "error")
            return redirect(url_for("auth.login"))
        return vista(*args, **kwargs)

    return envoltura