"""Pruebas de EstrategiaModeloLocal (responsable: Andres Coero Borga).

No se hacen llamadas reales. Si la clase recibe parámetros (dirección y nombre del
modelo), sumar acá pruebas que los usen.
"""
from plataforma_qa.estrategias.estrategia_modelo_local import EstrategiaModeloLocal


def test_define_generar_texto():
    assert callable(getattr(EstrategiaModeloLocal, "generar_texto", None))
