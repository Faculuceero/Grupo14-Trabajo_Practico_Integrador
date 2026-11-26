"""Roles y permisos: un solo lugar donde se decide quién es administrador.

Rol "usuario" (por defecto): crea preguntas y respuestas, edita y borra solo
lo suyo, y acepta respuestas solo en sus propias preguntas.
Rol "admin" (moderador): lo mismo, y además borra cualquier pregunta o
respuesta y gestiona las categorías.

El rol vive en la columna User.rol (texto). Si más adelante se quiere usar
la clase TipoRol del dominio, alcanza con cambiar es_admin().
"""

ROL_USUARIO = "usuario"
ROL_ADMIN = "admin"


def es_admin(usuario) -> bool:
    return usuario is not None and str(usuario.rol).strip().lower() == ROL_ADMIN


def exigir_admin(usuario, accion="realizar esta acción") -> None:
    """Lanza PermissionError (HTTP 403) si el usuario no es administrador."""
    if not es_admin(usuario):
        raise PermissionError(f"Solo un administrador puede {accion}.")