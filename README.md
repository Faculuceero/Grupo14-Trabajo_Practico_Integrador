Grupo14-Trabajo_Practico_Integrador

# Integrantes 
Lucero Facundo | 46.887.409 | faculucero035@gmail.com 
Migliorini Nicolas | 46.454.320 | nicomigliorini010@gmail.com 
Coero Borga German | 44.472.805 | germancoeroborga5@gmail.com 
Coero Borga Andres | 44.472.804 | andrescoero@gmail.com

Justificación del Trabajo Patrón Strategy: Se utiliza el patron Strategy para encapsular y desacoplar los diferentes modelos de la Inteligencia Artificial como comportamientos intercambiables. Cada modelo implementa una interfaz común orientada a recibir un prompt y retornar una respuesta generada. De este modo, la arquitectura cumple con el principio abierto/cerrado, facilitando la incorporación de nuevos modelos o proveedores simplemente implementando una nueva clase sin modificar la lógica existente del sistema.

Patrón Factory Method: Se utilizó el patrón Factory Method para delegar la creación de las instancias concretas de los autores del sistema. Dado que no se requiere construir familias de objetos dependientes entre sí, este enfoque simplifica la instanciación de la entidad Autor según las necesidades puntuales, centralizando la lógica de creación sin acoplar el código cliente a clases concretas.

# Plataforma colaborativa de Preguntas y Respuestas (Q&A) – Grupo 14

Plataforma de preguntas y respuestas para estudiantes universitarios. Las preguntas pueden recibir respuestas de usuarios o de un agente de IA. El diseño aplica **Factory Method** (creación de autores) y **Strategy** (proveedores de IA).

El diagrama de clases final está en la carpeta `docs/`.

## Integrantes y responsabilidades

| Integrante | Clases |
|---|---|
| German Coero Borga | `Autor`, `FabricaAutor`, `TextoEnriquecido`, `Categoria`, `Etiqueta` |
| Facu Lucero | `Publicacion`, `Voto`, `Pregunta`, `Respuesta`, `AgenteIA` |
| Andres Coero Borga | `EstrategiaLLM`, `EstrategiaOpenAI`, `EstrategiaGemini`, `EstrategiaModeloLocal`, `TipoVoto` |
| Nico Migliorini | `Usuario`, `Rol`, `TipoRol`, `FabricaUsuario`, `FabricaAgenteIA` |

Cada archivo `.py` tiene arriba el nombre de su responsable y el issue que le corresponde.

## Estructura del proyecto

```
├── plataforma_qa/
│   ├── autores/          Autor, Usuario, AgenteIA, Rol, TipoRol
│   ├── publicaciones/    Publicacion, Pregunta, Respuesta, Voto, TipoVoto,
│   │                     TextoEnriquecido, Categoria, Etiqueta
│   ├── fabricas/         FabricaAutor, FabricaUsuario, FabricaAgenteIA   (Factory Method)
│   └── estrategias/      EstrategiaLLM, EstrategiaOpenAI, EstrategiaGemini,
│                         EstrategiaModeloLocal                           (Strategy)
├── tests/                un archivo de pruebas por clase (+ conftest.py y utils.py)
├── docs/                 diagrama de clases
└── README.md
```
## Agente de IA

El agente responde preguntas de forma automática:
- al crear o editar una pregunta con la etiqueta `ia-help`;
- con el botón **Pedir respuesta al agente IA** (preguntas sin respuestas);
- con el comando `uv run flask --app plataforma_qa responder-pendientes --minutos 30`,
  que responde las preguntas sin respuestas publicadas hace al menos esos minutos;
- por API: `POST /api/preguntas/<id>/respuesta-ia`.

Nunca responde dos veces la misma pregunta. Si el proveedor falla, no se guarda ninguna respuesta.

Se configura con variables de entorno (las claves **nunca** se suben al repositorio):

| Variable | Para qué |
|---|---|
| `IA_PROVEEDOR` | `gemini` (por defecto), `openai` o `local` |
| `GEMINI_API_KEY` / `OPENAI_API_KEY` | clave del proveedor elegido |
| `IA_AGENTE_NOMBRE` | nombre que se muestra (por defecto "Asistente IA") |

## API de usuarios y autenticación

| Método | Ruta | Qué hace | Sesión |
|---|---|---|---|
| POST | `/api/auth/register` | Crea el usuario y abre sesión | No |
| POST | `/api/auth/login` | Abre sesión | No |
| POST | `/api/auth/logout` | Cierra sesión | No |
| GET | `/api/auth/me` | Usuario de la sesión | Sí |
| GET | `/api/users` · `/api/users/<id>` | Lista / detalle (datos públicos) | No |
| PATCH | `/api/users/<id>` | Cambiar el propio nombre | Sí |