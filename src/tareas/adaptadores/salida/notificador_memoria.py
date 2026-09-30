"""Adaptador de salida: recuerda los avisos en una lista.

Pensado para pruebas: permite comprobar qué avisos se enviaron sin efectos externos.
"""

from tareas.aplicacion.puertos import NotificadorTareas
from tareas.dominio.tarea import Tarea


class NotificadorMemoria(NotificadorTareas):
    def __init__(self) -> None:
        self.completadas: list[Tarea] = []

    def tarea_completada(self, tarea: Tarea) -> None:
        self.completadas.append(tarea)
