"""Comandos de terminal: uv run flask --app plataforma_qa <comando>"""

import click
from flask.cli import with_appcontext

from plataforma_qa.services import agente_ia


@click.command("responder-pendientes")
@click.option(
    "--minutos",
    default=agente_ia.MINUTOS_POR_DEFECTO,
    show_default=True,
    type=click.IntRange(min=0),
    help="Responde las preguntas sin respuestas publicadas hace al menos estos minutos.",
)
@with_appcontext
def responder_pendientes(minutos):
    """El agente IA responde las preguntas pendientes (#ia-help o sin responder)."""
    respondidas, fallidas = agente_ia.responder_pendientes(minutos)
    click.echo(f"Preguntas respondidas por el agente IA: {len(respondidas)}")
    for pregunta_id, motivo in fallidas:
        click.echo(f"  - No se pudo responder la pregunta {pregunta_id}: {motivo}")