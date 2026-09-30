"""Pruebas del adaptador de entrada por línea de comandos."""

from tareas.adaptadores.entrada.cli import ejecutar
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.aplicacion.servicio_tareas import ServicioTareas


def test_crear_y_listar(capsys):
    servicio = ServicioTareas(RepositorioMemoria())
    assert ejecutar(servicio, ["crear", "Estudiar"]) == 0
    assert ejecutar(servicio, ["listar"]) == 0
    assert "[ ] #1 Estudiar" in capsys.readouterr().out


def test_error_de_dominio_devuelve_codigo_1(capsys):
    servicio = ServicioTareas(RepositorioMemoria())
    assert ejecutar(servicio, ["eliminar", "99"]) == 1
    assert "No existe la tarea" in capsys.readouterr().out
