"""Errores del dominio.

Son excepciones propias del negocio. No dependen de HTTP ni de ninguna base de datos:
cada adaptador decide cómo traducirlas (por ejemplo, a un código 404 o 422).
"""


class ErrorDeDominio(Exception):
    """Clase base de todos los errores del negocio."""


class TareaNoEncontrada(ErrorDeDominio):
    """Se intentó operar sobre una tarea que no existe."""

    def __init__(self, tarea_id: int) -> None:
        super().__init__(f"No existe la tarea con id {tarea_id}")
        self.tarea_id = tarea_id


class TituloInvalido(ErrorDeDominio):
    """El título de la tarea está vacío o es demasiado largo."""
