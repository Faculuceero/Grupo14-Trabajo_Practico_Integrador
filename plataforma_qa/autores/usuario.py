"""Usuario (hereda de Autor)

Responsable: Nico Migliorini
Issue: "Implementar la clase Usuario"
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from plataforma_qa.autores.autor import Autor

if TYPE_CHECKING:
    from plataforma_qa.autores.rol import Rol
    from plataforma_qa.publicaciones.categoria import Categoria
    from plataforma_qa.publicaciones.etiqueta import Etiqueta
    from plataforma_qa.publicaciones.pregunta import Pregunta
    from plataforma_qa.publicaciones.publicacion import Publicacion
    from plataforma_qa.publicaciones.respuesta import Respuesta
    from plataforma_qa.publicaciones.texto_enriquecido import TextoEnriquecido
    from plataforma_qa.publicaciones.tipo_voto import TipoVoto
    from plataforma_qa.publicaciones.voto import Voto


class Usuario(Autor):
    def __init__(self, id: int, nombre_visible: str, email: str,
                 password_hash: str, rol: Rol) -> None:
        # TODO: validar los datos (el email debe ser único)
        super().__init__(id, nombre_visible)
        self._email = email                    # -email: String
        self._password_hash = password_hash    # -passwordHash: String (nunca la contraseña en texto plano)
        self._rol = rol                        # relación: tiene 1 Rol

    def autenticar(self, password: str) -> bool:
        raise NotImplementedError

    def preguntar(self, titulo: str, cuerpo: TextoEnriquecido, categoria: Categoria,
                  etiquetas: list[Etiqueta]) -> Pregunta:
        raise NotImplementedError

    def responder(self, p: Pregunta, cuerpo: TextoEnriquecido) -> Respuesta:
        raise NotImplementedError

    def votar(self, pub: Publicacion, tipo: TipoVoto) -> Voto:
        raise NotImplementedError
