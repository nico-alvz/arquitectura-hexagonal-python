"""Casos de uso (puerto de entrada) del CRUD de tareas.

Esta clase orquesta la lógica de la aplicación. Solo conoce el *puerto*
`RepositorioTareas`, nunca una base de datos concreta. Por eso se puede probar
con un repositorio falso en memoria, sin levantar nada.
"""

from tareas.aplicacion.puertos import NotificadorTareas, RepositorioTareas
from tareas.dominio.errores import TareaNoEncontrada
from tareas.dominio.tarea import Tarea


class ServicioTareas:
    """Operaciones CRUD sobre tareas."""

    def __init__(
        self,
        repositorio: RepositorioTareas,
        notificador: NotificadorTareas | None = None,
    ) -> None:
        # Inyección de dependencias: nos entregan los puertos ya construidos.
        # El notificador es opcional: sin él, simplemente no se avisa a nadie.
        self._repositorio = repositorio
        self._notificador = notificador

    # C — Create
    def crear(self, titulo: str, descripcion: str = "") -> Tarea:
        tarea = Tarea(titulo=titulo, descripcion=descripcion)  # Valida las reglas del dominio.
        return self._repositorio.guardar(tarea)

    # R — Read
    def obtener(self, tarea_id: int) -> Tarea:
        tarea = self._repositorio.obtener(tarea_id)
        if tarea is None:
            raise TareaNoEncontrada(tarea_id)
        return tarea

    def listar(self) -> list[Tarea]:
        return self._repositorio.listar()

    # U — Update
    def actualizar(
        self,
        tarea_id: int,
        titulo: str | None = None,
        descripcion: str | None = None,
        completada: bool | None = None,
    ) -> Tarea:
        """Actualiza solo los campos recibidos (los `None` se dejan como estaban)."""
        tarea = self.obtener(tarea_id)
        estaba_completada = tarea.completada
        if titulo is not None:
            Tarea.validar_titulo(titulo)
            tarea.titulo = titulo
        if descripcion is not None:
            tarea.descripcion = descripcion
        if completada is not None:
            tarea.completada = completada
        guardada = self._repositorio.guardar(tarea)
        # Regla de la aplicación: se avisa solo en la transición pendiente -> completada.
        if guardada.completada and not estaba_completada and self._notificador:
            self._notificador.tarea_completada(guardada)
        return guardada

    # D — Delete
    def eliminar(self, tarea_id: int) -> None:
        if not self._repositorio.eliminar(tarea_id):
            raise TareaNoEncontrada(tarea_id)
