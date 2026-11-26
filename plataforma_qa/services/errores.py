"""Errores de negocio que la API traduce a códigos HTTP.

    ValueError      -> 400  (datos inválidos)
    PermissionError -> 403  (no tiene permiso)
    NoEncontrado    -> 404
    Conflicto       -> 409  (por ejemplo, un nombre repetido)
    AgenteIAError   -> 502  (falló el proveedor de IA)
"""


class NoEncontrado(LookupError):
    """No existe lo que se pidió."""


class Conflicto(Exception):
    """La operación choca con el estado actual de los datos."""


class AgenteIAError(RuntimeError):
    """El agente de IA no pudo generar la respuesta."""