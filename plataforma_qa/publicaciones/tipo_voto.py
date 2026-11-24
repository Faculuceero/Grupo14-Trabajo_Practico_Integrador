"""TipoVoto («enumeration»)

Responsable: Andres Coero Borga
Issue: "Implementar la enumeración TipoVoto"

TODO: definir los dos valores del diagrama: POSITIVO y NEGATIVO.
"""

from enum import Enum


class TipoVoto(Enum):
    POSITIVO = "POSITIVO"
    NEGATIVO = "NEGATIVO"
