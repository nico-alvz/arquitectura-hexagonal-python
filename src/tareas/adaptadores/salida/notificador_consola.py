"""Adaptador de salida: imprime los avisos en la consola.

Es la implementación más simple del puerto `NotificadorTareas`. Para enviar correos
o mensajes bastaría con escribir otra clase que implemente el mismo contrato.
"""

from tareas.aplicacion.puertos import NotificadorTareas
from tareas.dominio.tarea import Tarea


class NotificadorConsola(NotificadorTareas):
    def tarea_completada(self, tarea: Tarea) -> None:
        print(f"🎉 Tarea completada: #{tarea.id} {tarea.titulo}")
