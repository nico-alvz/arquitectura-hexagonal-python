"""Casos de uso (puerto de entrada) del CRUD de tareas.

Esta clase orquesta la lógica de la aplicación. Solo conoce el *puerto*
`RepositorioTareas`, nunca una base de datos concreta. Por eso se puede probar
con un repositorio falso en memoria, sin levantar nada.
"""

from tareas.aplicacion.puertos import RepositorioTareas
from tareas.dominio.errores import TareaNoEncontrada
from tareas.dominio.tarea import Tarea


class ServicioTareas:
    """Operaciones CRUD sobre tareas."""

    def __init__(self, repositorio: RepositorioTareas) -> None:
        # Inyección de dependencias: nos entregan el repositorio ya construido.
        self._repositorio = repositorio

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
        if titulo is not None:
            Tarea.validar_titulo(titulo)
            tarea.titulo = titulo
        if descripcion is not None:
            tarea.descripcion = descripcion
        if completada is not None:
            tarea.completada = completada
        return self._repositorio.guardar(tarea)

    # D — Delete
    def eliminar(self, tarea_id: int) -> None:
        if not self._repositorio.eliminar(tarea_id):
            raise TareaNoEncontrada(tarea_id)
