"""Validaciones de texto compartidas por los servicios."""

MAX_TITULO = 200
MAX_CATEGORIA = 100
MAX_ETIQUETA = 50


def texto_obligatorio(valor, campo, maximo=None) -> str:
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El campo '{campo}' es obligatorio.")
    limpio = valor.strip()
    if maximo is not None and len(limpio) > maximo:
        raise ValueError(f"El campo '{campo}' admite hasta {maximo} caracteres.")
    return limpio


def normalizar_etiquetas(nombres) -> list[str]:
    """Devuelve los nombres sin '#', en minúsculas, sin repetidos ni vacíos."""
    if nombres is None:
        return []
    if not isinstance(nombres, (list, tuple)):
        raise ValueError("Las etiquetas deben enviarse como una lista.")  # noqa: TRY004
    resultado = []
    for nombre in nombres:
        if not isinstance(nombre, str):
            raise ValueError("Cada etiqueta debe ser un texto.")  # noqa: TRY004
        limpio = nombre.strip().lstrip("#").strip().lower()
        if not limpio:
            continue
        if len(limpio) > MAX_ETIQUETA:
            raise ValueError(f"Cada etiqueta admite hasta {MAX_ETIQUETA} caracteres.")
        if limpio not in resultado:
            resultado.append(limpio)
    return resultado