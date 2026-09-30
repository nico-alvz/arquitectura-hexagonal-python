"""Raíz de composición: el único lugar donde se "conectan los cables".

Aquí se elige qué adaptador de salida usar, se inyecta en el servicio y el servicio
en el adaptador de entrada. Para cambiar de base de datos solo se toca este archivo.

Variable de entorno:
    REPOSITORIO   "sqlite" (por defecto) o "memoria"
    RUTA_DB       ruta del archivo SQLite (por defecto "tareas.db")
"""

import os

from tareas.adaptadores.entrada.api_fastapi import crear_app
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from tareas.aplicacion.puertos import RepositorioTareas
from tareas.aplicacion.servicio_tareas import ServicioTareas


def construir_repositorio() -> RepositorioTareas:
    if os.getenv("REPOSITORIO", "sqlite") == "memoria":
        return RepositorioMemoria()
    return RepositorioSQLite(os.getenv("RUTA_DB", "tareas.db"))


app = crear_app(ServicioTareas(construir_repositorio()))
