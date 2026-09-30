"""Pruebas unitarias del núcleo: sin HTTP y sin base de datos real."""

import pytest

from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.aplicacion.servicio_tareas import ServicioTareas
from tareas.dominio.errores import TareaNoEncontrada, TituloInvalido


@pytest.fixture
def servicio() -> ServicioTareas:
    return ServicioTareas(RepositorioMemoria())


def test_crear_asigna_id_y_queda_pendiente(servicio):
    tarea = servicio.crear("Estudiar arquitectura hexagonal")
    assert tarea.id == 1
    assert tarea.completada is False


def test_crear_con_titulo_vacio_falla(servicio):
    with pytest.raises(TituloInvalido):
        servicio.crear("   ")


def test_listar_devuelve_todas(servicio):
    servicio.crear("A")
    servicio.crear("B")
    assert [t.titulo for t in servicio.listar()] == ["A", "B"]


def test_actualizar_solo_cambia_campos_recibidos(servicio):
    tarea = servicio.crear("Original", "detalle")
    actualizada = servicio.actualizar(tarea.id, completada=True)
    assert actualizada.completada is True
    assert actualizada.titulo == "Original"
    assert actualizada.descripcion == "detalle"


def test_actualizar_inexistente_falla(servicio):
    with pytest.raises(TareaNoEncontrada):
        servicio.actualizar(99, titulo="X")


def test_eliminar_y_luego_no_existe(servicio):
    tarea = servicio.crear("Temporal")
    servicio.eliminar(tarea.id)
    with pytest.raises(TareaNoEncontrada):
        servicio.obtener(tarea.id)
