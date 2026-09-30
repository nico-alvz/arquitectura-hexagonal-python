"""Raíz de composición de la línea de comandos.

Ejemplo: python -m tareas.principal_cli crear "Estudiar"
"""

import sys

from tareas.adaptadores.entrada.cli import ejecutar
from tareas.composicion import construir_servicio

if __name__ == "__main__":
    sys.exit(ejecutar(construir_servicio(), sys.argv[1:]))
