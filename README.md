Grupo14-Trabajo_Practico_Integrador

Integrantes:
 Lucero Facundo | 46.887.409 | faculucero035@gmail.com 
 Migliorini Nicolas | 46.454.320 | nicomigliorini010@gmail.com 
 Coero Borga German | 44.472.805 | germancoeroborga5@gmail.com 
 Coero Borga Andres | 44.472.804 | andrescoero@gmail.com 

 Justificación del Trabajo
 Patrón Strategy: Se utiliza el patron Strategy para encapsular y desacoplar los diferentes modelos de la Inteligencia Artificial como comportamientos intercambiables.
 Cada modelo implementa una interfaz común orientada a recibir un prompt y retornar una respuesta generada. 
 De este modo, la arquitectura cumple con el principio abierto/cerrado, facilitando la incorporación de nuevos modelos o proveedores simplemente implementando una nueva clase sin modificar la lógica existente del sistema.

 Patrón Factory Method: Se utilizó el patrón Factory Method para delegar la creación de las instancias concretas de los autores del sistema. 
 Dado que no se requiere construir familias de objetos dependientes entre sí, este enfoque simplifica la instanciación de la entidad Autor según las necesidades puntuales, 
 centralizando la lógica de creación sin acoplar el código cliente a clases concretas.
