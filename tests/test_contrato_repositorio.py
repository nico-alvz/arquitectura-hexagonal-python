"""Pruebas de contrato: TODA implementación de `RepositorioTareas` debe pasarlas.

Al crear un adaptador nuevo, agrégalo a la fixture `repositorio` y comprueba que
se comporta igual que los demás.
"""

import pytest

from tareas.adaptadores.salida.repositorio_json import RepositorioJSON
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from tareas.dominio.tarea import Tarea


@pytest.fixture(params=["memoria", "sqlite", "json"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        return RepositorioMemoria()
    if request.param == "sqlite":
        return RepositorioSQLite(":memory:")
    return RepositorioJSON(tmp_path / "tareas.json")


def test_guardar_nueva_asigna_id(repositorio):
    tarea = repositorio.guardar(Tarea(titulo="A"))
    assert tarea.id is not None


def test_ids_son_distintos(repositorio):
    a = repositorio.guardar(Tarea(titulo="A"))
    b = repositorio.guardar(Tarea(titulo="B"))
    assert a.id != b.id


def test_obtener_devuelve_lo_guardado(repositorio):
    guardada = repositorio.guardar(Tarea(titulo="A", descripcion="d", completada=True))
    assert repositorio.obtener(guardada.id) == guardada


def test_obtener_inexistente_devuelve_none(repositorio):
    assert repositorio.obtener(999) is None


def test_guardar_existente_actualiza(repositorio):
    tarea = repositorio.guardar(Tarea(titulo="A"))
    tarea.titulo = "B"
    repositorio.guardar(tarea)
    assert repositorio.obtener(tarea.id).titulo == "B"
    assert len(repositorio.listar()) == 1


def test_listar_ordenado_por_id(repositorio):
    repositorio.guardar(Tarea(titulo="A"))
    repositorio.guardar(Tarea(titulo="B"))
    ids = [t.id for t in repositorio.listar()]
    assert ids == sorted(ids)


def test_eliminar_devuelve_si_existia(repositorio):
    tarea = repositorio.guardar(Tarea(titulo="A"))
    assert repositorio.eliminar(tarea.id) is True
    assert repositorio.eliminar(tarea.id) is False
    assert repositorio.obtener(tarea.id) is None
