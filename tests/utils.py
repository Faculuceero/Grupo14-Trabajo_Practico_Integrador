"""Ayudas compartidas por los tests (no son pruebas)."""

import hashlib
from datetime import datetime, timedelta

from plataforma_qa.autores.rol import Rol
from plataforma_qa.autores.tipo_rol import TipoRol
from plataforma_qa.autores.usuario import Usuario
from plataforma_qa.estrategias.estrategia_llm import EstrategiaLLM


def hash_password(password: str) -> str:
    """Acuerdo del equipo: passwordHash = SHA-256 (hexadecimal) de la contraseña."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def crear_usuario(n: int = 1) -> Usuario:
    """Usuario distinto para cada número n (id, nombre y email únicos)."""
    return Usuario(
        n,
        f"usuario{n}",
        f"usuario{n}@mail.com",
        hash_password("clave"),
        Rol(TipoRol.USUARIO_GENERAL),
    )


def hace_minutos(minutos: int) -> datetime:
    return datetime.now() - timedelta(minutes=minutos)


class EstrategiaFalsa(EstrategiaLLM):
    """Proveedor de IA de mentira: devuelve un texto fijo y recuerda los prompts."""

    def __init__(self, texto: str = "respuesta falsa") -> None:
        self.texto = texto
        self.prompts: list[str] = []

    def generar_texto(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.texto


class EstrategiaFallida(EstrategiaLLM):
    """Proveedor de IA que siempre falla (para probar el manejo de errores)."""

    def generar_texto(self, prompt: str) -> str:
        raise RuntimeError("falló el proveedor de IA")


def datos_usuario(**cambios) -> dict:
    """Datos válidos para FabricaUsuario.crear_autor (se pueden pisar con cambios)."""
    datos = {"id": 1, "nombre": "Ana", "email": "ana@mail.com", "password": "secreta"}
    datos.update(cambios)
    return datos


def datos_agente(**cambios) -> dict:
    """Datos válidos para FabricaAgenteIA.crear_autor (se pueden pisar con cambios)."""
    datos = {
        "id": 99,
        "nombre": "Asistente IA",
        "etiqueta": "ia-help",
        "minutos_sin_respuesta": 30,
        "estrategia": EstrategiaFalsa(),
    }
    datos.update(cambios)
    return datos
