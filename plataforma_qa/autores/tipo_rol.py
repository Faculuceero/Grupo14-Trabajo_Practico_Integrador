"""TipoRol («enumeration»)

Responsable: Nico Migliorini
Issue: "Implementar la enumeración TipoRol"

TODO: definir los dos valores del diagrama: ADMIN y USUARIO_GENERAL.
"""
from enum import Enum


class TipoRol(Enum):
    ADMIN = "ADMIN"
    USUARIO_GENERAL = "USUARIO_GENERAL"