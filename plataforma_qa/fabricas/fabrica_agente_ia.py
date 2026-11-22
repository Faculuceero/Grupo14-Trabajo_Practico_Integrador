"""FabricaAgenteIA (hereda de FabricaAutor) - ConcreteCreator

Responsable: Nico Migliorini
Issue: "Implementar la clase FabricaAgenteIA"
"""

from __future__ import annotations

from plataforma_qa.autores.agente_ia import AgenteIA
from plataforma_qa.fabricas.fabrica_autor import FabricaAutor


class FabricaAgenteIA(FabricaAutor):
    def crear_autor(self, datos: dict) -> AgenteIA:
        """Crea y devuelve un AgenteIA válido a partir del diccionario `datos`."""
        if not isinstance(datos, dict):
            raise ValueError("Los datos del agente IA deben enviarse en un diccionario.")

        if "id" not in datos or datos["id"] is None:
            raise ValueError("Falta el dato obligatorio: 'id'.")

        nombre = datos.get("nombre") if "nombre" in datos else datos.get("nombre_visible")
        if not nombre or not str(nombre).strip():
            raise ValueError("Falta el dato obligatorio: 'nombre'.")

        etiqueta = datos.get("etiqueta")
        if not etiqueta or not str(etiqueta).strip():
            raise ValueError("Falta el dato obligatorio: 'etiqueta'.")

        minutos = (
            datos.get("minutos_sin_respuesta")
            if "minutos_sin_respuesta" in datos
            else datos.get("minutosSinRespuesta")
        )
        if minutos is None:
            raise ValueError("Falta el dato obligatorio: 'minutos_sin_respuesta'.")
        if not isinstance(minutos, int) or isinstance(minutos, bool) or minutos < 0:
            raise ValueError("El campo 'minutos_sin_respuesta' debe ser un entero mayor o igual a cero.")

        if "estrategia" not in datos or datos["estrategia"] is None:
            raise ValueError("Falta el dato obligatorio: 'estrategia'.")

        return AgenteIA(
            id=datos["id"],
            nombre_visible=str(nombre).strip(),
            etiqueta=str(etiqueta).strip(),
            minutos_sin_respuesta=minutos,
            estrategia=datos["estrategia"],
        )

    def crearAutor(self, datos: dict) -> AgenteIA:
        """Alias en camelCase según diagrama UML."""
        return self.crear_autor(datos)