"""Entidad `Tarea`: el corazón del dominio.

Python puro: sin FastAPI, sin SQL, sin librerías externas.
Aquí viven las reglas de negocio que siempre deben cumplirse.
"""

from dataclasses import dataclass

from tareas.dominio.errores import TituloInvalido

LARGO_MAXIMO_TITULO = 100


@dataclass
class Tarea:
    """Una tarea pendiente (o terminada) de una lista de tareas."""

    titulo: str
    descripcion: str = ""
    completada: bool = False
    id: int | None = None  # Lo asigna el repositorio al guardar por primera vez.

    def __post_init__(self) -> None:
        self.validar_titulo(self.titulo)

    @staticmethod
    def validar_titulo(titulo: str) -> None:
        """Regla de negocio: el título es obligatorio y tiene un largo máximo."""
        if not titulo or not titulo.strip():
            raise TituloInvalido("El título no puede estar vacío")
        if len(titulo) > LARGO_MAXIMO_TITULO:
            raise TituloInvalido(f"El título no puede superar {LARGO_MAXIMO_TITULO} caracteres")

    def completar(self) -> None:
        """Marca la tarea como terminada."""
        self.completada = True
