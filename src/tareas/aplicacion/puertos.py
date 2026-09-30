"""Puertos: los contratos que el núcleo necesita del mundo exterior.

Un *puerto* es solo una interfaz. El núcleo dice "necesito guardar y buscar tareas"
sin saber si eso ocurre en memoria, en SQLite o en PostgreSQL.
Los adaptadores de la carpeta `adaptadores/salida` implementan este contrato.
"""

from abc import ABC, abstractmethod

from tareas.dominio.tarea import Tarea


class RepositorioTareas(ABC):
    """Puerto de salida: persistencia de tareas."""

    @abstractmethod
    def guardar(self, tarea: Tarea) -> Tarea:
        """Crea la tarea (si no tiene id) o la actualiza. Devuelve la tarea guardada."""

    @abstractmethod
    def obtener(self, tarea_id: int) -> Tarea | None:
        """Devuelve la tarea o `None` si no existe."""

    @abstractmethod
    def listar(self) -> list[Tarea]:
        """Devuelve todas las tareas ordenadas por id."""

    @abstractmethod
    def eliminar(self, tarea_id: int) -> bool:
        """Elimina la tarea. Devuelve `True` si existía."""
