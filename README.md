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

## Cómo correr las pruebas

Parados en la carpeta del proyecto:

```bash
# Si usan uv:
uv run --with pytest python -m pytest

# Si usan Python con pip:
pip install pytest
python -m pytest
```

Para correr solo las pruebas de una clase: `python -m pytest tests/test_categoria.py`

## Cómo leer el resultado de las pruebas

Los tests ya están escritos y describen lo que debe hacer cada clase (son los criterios de aceptación de los issues). Al principio **muchos fallan**, y es lo esperado: las clases todavía no están implementadas.

El trabajo de cada integrante es lograr que **los tests de sus clases pasen**. Cuando todos pasan, el issue está listo para pasar a **In Review**.

Un test que falla con `NotImplementedError` significa que falta implementar ese método. Si un test no refleja bien lo que el equipo decidió, se puede corregir, pero hay que avisar a los demás.

## Flujo de trabajo para cada issue

1. Pasar el issue a **In Progress** en el Project.
2. Crear una rama: `git checkout -b feature/nombre-de-la-clase`
3. Implementar la clase y hacer commits que mencionen el issue: `git commit -m "Add clase Categoria (#12)"`
4. Subir la rama y abrir un **Pull Request** con `Closes #12` en la descripción. Pasar el issue a **In Review**.
5. Otro integrante revisa el PR y verifica los criterios de aceptación. Al hacer merge a `main`, el issue se cierra y pasa a **Done**.

No se trabaja directamente sobre `main`, y cada integrante modifica solo los archivos de sus clases (para evitar conflictos).

## Acuerdos del equipo

Estas decisiones no están en el diagrama, pero las clases dependen unas de otras y los tests las suponen.

**Errores.** Se usan estas excepciones de Python:
- `ValueError`: datos inválidos (nombre vacío, email sin `@`, falta un dato obligatorio, votar dos veces la misma publicación).
- `PermissionError`: el usuario no tiene permiso (aceptar una respuesta de una pregunta ajena).
- `RuntimeError`: falla un proveedor de IA (falta la clave de API, no hay conexión).
- `TypeError`: se instancia una clase abstracta o se pasa un objeto de tipo incorrecto.

**Contraseñas.** `passwordHash` es el SHA-256 en hexadecimal de la contraseña (`hashlib.sha256(password.encode()).hexdigest()`). Nunca se guarda la contraseña en texto plano.

**Datos que reciben las fábricas** (`crear_autor(datos)`, donde `datos` es un diccionario):

| Fábrica | Claves obligatorias | Claves opcionales |
|---|---|---|
| `FabricaUsuario` | `nombre`, `email`, `password` | `id`, `rol` (un `TipoRol`; por defecto `USUARIO_GENERAL`) |
| `FabricaAgenteIA` | `nombre`, `etiqueta`, `minutos_sin_respuesta`, `estrategia` | `id` |

**Email único.** `FabricaUsuario` recuerda los emails que ya creó y rechaza repetidos con `ValueError`.

**Votos.** Un usuario no puede votar dos veces la misma publicación. Lo controla `Publicacion.agregar_voto`.

**Agente de IA.**
- La etiqueta del agente se escribe sin `#` (por ejemplo `ia-help`).
- `debe_responder` es verdadero si la pregunta tiene esa etiqueta, o si no tiene respuestas y pasaron `minutos_sin_respuesta` desde que se publicó.
- El agente no responde dos veces la misma pregunta.
- Si la estrategia falla, no se crea ninguna respuesta.

**Claves de API.** Nunca se suben al repositorio. Se leen de variables de entorno: `OPENAI_API_KEY` para OpenAI y `GEMINI_API_KEY` (o `GOOGLE_API_KEY`) para Gemini.

## Convenciones del código

- **Nombres en Python:** las clases se llaman igual que en el diagrama. Los métodos y atributos pasan a `snake_case`: `calcularPuntuacion()` → `calcular_puntuacion()`, `nombreVisible` → `_nombre_visible`.
- **Visibilidad:** los atributos privados (`-`) y protegidos (`#`) del diagrama se escriben con un guion bajo adelante (`self._nombre`). Los tests leen esos atributos directamente.
- **Esqueletos:** los métodos que faltan implementar lanzan `NotImplementedError`. Al implementarlos, se elimina esa línea. Los comentarios `# TODO` marcan lo que falta en cada clase.
- **Constructores:** los parámetros de `__init__` son una propuesta. Si alguien necesita cambiarlos, avisa al resto del equipo y actualiza los tests, porque otras clases los usan.
- **Métodos auxiliares:** `Publicacion.agregar_voto` y `Pregunta.agregar_respuesta` no figuran en el diagrama, pero hacen falta para que `Usuario.votar` y `Usuario.responder` puedan asociar objetos.
- **Imports entre clases:** para nombrar clases de otros archivos solo como tipo se usa `TYPE_CHECKING` (ya está armado en los esqueletos). Esto evita errores de importación circular.
