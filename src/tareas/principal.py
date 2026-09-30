"""Raíz de composición de la API: el único lugar donde se "conectan los cables".

La elección de adaptadores está en `composicion.py`. Para cambiar de base de datos
solo se toca allí (o se define la variable de entorno `REPOSITORIO`).

Ejecución: uvicorn tareas.principal:app
"""

from tareas.adaptadores.entrada.api_fastapi import crear_app
from tareas.composicion import construir_servicio

app = crear_app(construir_servicio())
