"""Construcción del servicio con sus adaptadores (compartida por API y CLI).

Variables de entorno:
    REPOSITORIO   "sqlite" (por defecto), "json" o "memoria"
    RUTA_DB       ruta del archivo SQLite (por defecto "tareas.db")
    RUTA_JSON     ruta del archivo JSON (por defecto "tareas.json")
"""

import os

from tareas.adaptadores.salida.notificador_consola import NotificadorConsola
from tareas.adaptadores.salida.repositorio_json import RepositorioJSON
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from tareas.aplicacion.puertos import RepositorioTareas
from tareas.aplicacion.servicio_tareas import ServicioTareas


def construir_repositorio() -> RepositorioTareas:
    eleccion = os.getenv("REPOSITORIO", "sqlite")
    if eleccion == "memoria":
        return RepositorioMemoria()
    if eleccion == "json":
        return RepositorioJSON(os.getenv("RUTA_JSON", "tareas.json"))
    return RepositorioSQLite(os.getenv("RUTA_DB", "tareas.db"))


def construir_servicio() -> ServicioTareas:
    return ServicioTareas(construir_repositorio(), NotificadorConsola())
