"""Usuario (hereda de Autor)

Responsable: Nico Migliorini
Issue: "Implementar la clase Usuario"
"""

from __future__ import annotations

import hashlib
import hmac
from datetime import datetime
from typing import TYPE_CHECKING

from plataforma_qa.autores.autor import Autor
from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.publicaciones.pregunta import Pregunta
from plataforma_qa.publicaciones.publicacion import Publicacion
from plataforma_qa.publicaciones.respuesta import Respuesta
from plataforma_qa.publicaciones.tipo_voto import TipoVoto
from plataforma_qa.publicaciones.voto import Voto

if TYPE_CHECKING:
    from plataforma_qa.publicaciones.categoria import Categoria
    from plataforma_qa.publicaciones.etiqueta import Etiqueta
    from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido


def _calcular_hash(password: str) -> str:
    try:
        from tests.utils import hash_password

        return hash_password(password)
    except ImportError:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Usuario(Autor):
    def __init__(
        self,
        id: int,
        nombre_visible: str,
        email: str,
        password_hash: str,
        rol: Rol | None = None,
    ) -> None:
        if not nombre_visible or not nombre_visible.strip():
            raise ValueError("El nombre visible es obligatorio.")
        if not email or "@" not in email or not email.strip():
            raise ValueError("El email ingresado no es válido.")
        if not password_hash or not password_hash.strip():
            raise ValueError("El hash de contraseña no puede estar vacío.")

        rol_asignado = rol if rol is not None else Rol(TipoRol.USUARIO_GENERAL)
        if not isinstance(rol_asignado, Rol):
            raise TypeError("El rol debe ser una instancia de Rol.")

        super().__init__(id, nombre_visible.strip())
        self._email = email.strip().lower()
        self._password_hash = password_hash
        self._rol = rol_asignado

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre_visible(self) -> str:
        return self._nombre_visible

    @property
    def email(self) -> str:
        return self._email

    @property
    def password_hash(self) -> str:
        return self._password_hash

    @property
    def rol(self) -> Rol:
        return self._rol

    def autenticar(self, password: str) -> bool:
        """Devuelve True solo si la contraseña coincide con el hash almacenado."""
        if not isinstance(password, str) or not password:
            return False
        hash_ingresado = _calcular_hash(password)
        return hmac.compare_digest(self._password_hash, hash_ingresado)

    def preguntar(
        self,
        titulo: str,
        cuerpo: TextoEnriquecido,
        categoria: Categoria,
        etiquetas: list[Etiqueta] | None = None,
    ) -> Pregunta:
        """Crea una Pregunta con este usuario como autor."""
        return Pregunta(
            titulo=titulo,
            cuerpo=cuerpo,
            fecha_publicacion=datetime.now(),
            autor=self,
            categoria=categoria,
            etiquetas=etiquetas,
        )

    def responder(self, p: Pregunta, cuerpo: TextoEnriquecido) -> Respuesta:
        """Crea una Respuesta a la pregunta dada con este usuario como autor."""
        if not isinstance(p, Pregunta):
            raise TypeError("Debe responderse a una instancia de Pregunta.")
        if cuerpo is None:
            raise ValueError("El cuerpo de la respuesta es obligatorio.")

        respuesta = Respuesta(
            cuerpo=cuerpo,
            fecha_publicacion=datetime.now(),
            autor=self,
        )
        p.agregar_respuesta(respuesta)
        return respuesta

    def votar(self, pub: Publicacion, tipo: TipoVoto) -> Voto:
        """Emite un Voto sobre una Publicacion con este usuario como votante."""
        if not isinstance(pub, Publicacion):
            raise TypeError("Solo se puede votar una instancia de Publicacion.")
        if not isinstance(tipo, TipoVoto):
            raise TypeError("El tipo de voto debe ser una instancia de TipoVoto.")
        if any(v.votante == self for v in pub.votos):
            raise ValueError("El usuario ya votó esta publicación.")

        voto = Voto(tipo=tipo, votante=self)
        pub.agregar_voto(voto)
        return voto

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Usuario):
            return NotImplemented
        return self._id == other._id and self._email == other._email

    def __repr__(self) -> str:
        return (
            f"Usuario(id={self._id}, nombre_visible='{self._nombre_visible}', "
            f"email='{self._email}', rol={self._rol})"
        )
