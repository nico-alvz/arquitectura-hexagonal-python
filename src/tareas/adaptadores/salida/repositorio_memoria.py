"""Adaptador de salida: guarda las tareas en un diccionario en memoria.

Ideal para pruebas y demostraciones. Los datos se pierden al detener el programa.
"""

from dataclasses import replace

from tareas.aplicacion.puertos import RepositorioTareas
from tareas.dominio.tarea import Tarea


class RepositorioMemoria(RepositorioTareas):
    def __init__(self) -> None:
        self._tareas: dict[int, Tarea] = {}
        self._siguiente_id = 1

    def guardar(self, tarea: Tarea) -> Tarea:
        if tarea.id is None:
            tarea.id = self._siguiente_id
            self._siguiente_id += 1
        # Guardamos una copia para que cambios externos no alteren lo almacenado.
        self._tareas[tarea.id] = replace(tarea)
        return replace(tarea)

    def obtener(self, tarea_id: int) -> Tarea | None:
        tarea = self._tareas.get(tarea_id)
        return replace(tarea) if tarea else None

    def listar(self) -> list[Tarea]:
        return [replace(t) for _, t in sorted(self._tareas.items())]

    def eliminar(self, tarea_id: int) -> bool:
        return self._tareas.pop(tarea_id, None) is not None
