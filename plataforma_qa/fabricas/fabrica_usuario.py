"""FabricaUsuario (hereda de FabricaAutor) - ConcreteCreator

Responsable: Nico Migliorini
Issue: "Implementar la clase FabricaUsuario"
"""

from __future__ import annotations

import hashlib

from plataforma_qa.fabricas.fabrica_autor import FabricaAutor
from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.autores.usuario import Usuario


def _hashear_password(password: str) -> str:
    try:
        from tests.utils import hash_password
        return hash_password(password)
    except ImportError:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


class FabricaUsuario(FabricaAutor):
    def __init__(self) -> None:
        self._emails_registrados: set[str] = set()

    def crear_autor(self, datos: dict) -> Usuario:
        """Crea y devuelve un Usuario válido a partir del diccionario `datos`."""
        if not isinstance(datos, dict):
            raise ValueError("Los datos del usuario deben enviarse en un diccionario.")

        nombre = datos.get("nombre") if "nombre" in datos else datos.get("nombre_visible")
        if "id" not in datos or datos["id"] is None:
            raise ValueError("Falta el dato obligatorio: 'id'.")
        if not nombre or not str(nombre).strip():
            raise ValueError("Falta el dato obligatorio: 'nombre'.")
        if "email" not in datos or not datos["email"] or not str(datos["email"]).strip():
            raise ValueError("Falta el dato obligatorio: 'email'.")
        if "password" not in datos or not datos["password"] or not str(datos["password"]).strip():
            raise ValueError("Falta el dato obligatorio: 'password'.")

        email_normalizado = str(datos["email"]).strip().lower()
        if email_normalizado in self._emails_registrados:
            raise ValueError(f"El email '{datos['email']}' ya está registrado.")

        rol_dato = datos.get("rol")
        if rol_dato is None:
            rol = Rol(TipoRol.USUARIO_GENERAL)
        elif isinstance(rol_dato, TipoRol):
            rol = Rol(rol_dato)
        elif isinstance(rol_dato, Rol):
            rol = rol_dato
        else:
            raise TypeError("El campo 'rol' debe ser una instancia de TipoRol o Rol.")

        password_hash = _hashear_password(str(datos["password"]))
        usuario = Usuario(
            id=datos["id"],
            nombre_visible=str(nombre).strip(),
            email=email_normalizado,
            password_hash=password_hash,
            rol=rol,
        )
        self._emails_registrados.add(email_normalizado)
        return usuario

    def crearAutor(self, datos: dict) -> Usuario:
        """Alias en camelCase según diagrama UML."""
        return self.crear_autor(datos)