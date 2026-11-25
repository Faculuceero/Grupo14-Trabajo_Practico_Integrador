from __future__ import annotations

from typing import Any

from plataforma_qa.fabricas.fabrica_agente_ia import FabricaAgenteIA


class IAService:
    def __init__(self, fabrica_agente: FabricaAgenteIA | None = None) -> None:
        self._fabrica = fabrica_agente or FabricaAgenteIA()

    def generar_respuesta_automatica(
        self,
        pregunta_contexto: dict[str, Any],
        datos_agente: dict[str, Any],
    ) -> str:
        """Recibe el contexto de una pregunta (titulo, cuerpo) y los datos para instanciar un AgenteIA.

        Ejecuta la generación de respuesta capturando posibles errores de red o API keys faltantes.
        """
        titulo = pregunta_contexto.get("titulo", "").strip()
        cuerpo_raw = pregunta_contexto.get("cuerpo", "").strip()

        if not titulo or not cuerpo_raw:
            raise ValueError(
                "El contexto de la pregunta debe incluir 'titulo' y 'cuerpo' válidos."
            )

        try:
            agente = self._fabrica.crear_autor(datos_agente)
            prompt = f"Pregunta: {titulo}\nDetalle: {cuerpo_raw}"

            return agente.estrategia.generar_respuesta(prompt)

        except KeyError as e:
            return f"Error de configuración del agente: falta el campo obligatorio {e}."
        except Exception as e:  # noqa: BLE001
            return f"No se pudo completar la respuesta del Agente IA: {e!s}"