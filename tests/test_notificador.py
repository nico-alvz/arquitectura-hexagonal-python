"""Pruebas del segundo puerto: el notificador."""

from tareas.adaptadores.salida.notificador_memoria import NotificadorMemoria
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.aplicacion.servicio_tareas import ServicioTareas


def _servicio():
    notificador = NotificadorMemoria()
    return ServicioTareas(RepositorioMemoria(), notificador), notificador


def test_avisa_al_completar():
    servicio, notificador = _servicio()
    tarea = servicio.crear("A")
    servicio.actualizar(tarea.id, completada=True)
    assert [t.id for t in notificador.completadas] == [tarea.id]


def test_no_avisa_dos_veces():
    servicio, notificador = _servicio()
    tarea = servicio.crear("A")
    servicio.actualizar(tarea.id, completada=True)
    servicio.actualizar(tarea.id, completada=True)
    assert len(notificador.completadas) == 1


def test_no_avisa_si_no_se_completa():
    servicio, notificador = _servicio()
    tarea = servicio.crear("A")
    servicio.actualizar(tarea.id, titulo="B")
    assert notificador.completadas == []
