"""Reglas de negocio de los usuarios usadas por la API.

OJO: la web guarda y compara la contraseña tal cual (sin hash). Para que el
registro por web y por API sean compatibles, acá se hace lo mismo. Si algún día
se hashean las contraseñas, hay que cambiarlo en estos dos puntos:
crear_usuario (al guardar) y autenticar (al comparar).
"""

import hmac

from plataforma_qa.extensions import db
from plataforma_qa.models import User
from plataforma_qa.services.errores import Conflicto
from plataforma_qa.services.validacion import texto_obligatorio

MIN_PASSWORD = 8


def _por_email(email: str):
    return db.session.scalar(db.select(User).where(User.email == email))


def listar_usuarios() -> list[User]:
    return list(db.session.scalars(db.select(User).order_by(User.id)))


def crear_usuario(name, email, password) -> User:
    name = texto_obligatorio(name, "name", 120)
    email = texto_obligatorio(email, "email", 255).lower()
    if "@" not in email:
        raise ValueError("El email ingresado no es válido.")
    if not isinstance(password, str) or len(password) < MIN_PASSWORD:
        raise ValueError(f"La contraseña debe tener al menos {MIN_PASSWORD} caracteres.")
    if _por_email(email) is not None:
        raise Conflicto("Ya existe un usuario registrado con ese correo.")

    # El rol siempre es "usuario": un registro público no puede pedir ser admin.
    usuario = User(name=name, email=email, password=password, rol="usuario")
    db.session.add(usuario)
    db.session.commit()
    return usuario


def autenticar(email, password):
    """Devuelve el usuario si las credenciales son correctas; si no, None."""
    if not isinstance(email, str) or not isinstance(password, str):
        return None
    usuario = _por_email(email.strip().lower())
    if usuario is None:
        return None
    if not hmac.compare_digest(usuario.password.encode(), password.encode()):
        return None
    return usuario


def modificar_nombre(usuario, solicitante, name) -> User:
    if solicitante is None or solicitante.id != usuario.id:
        raise PermissionError("Solo podés modificar tu propio usuario.")
    usuario.name = texto_obligatorio(name, "name", 120)
    db.session.commit()
    return usuario