"""Pruebas de integración: API completa sobre SQLite en memoria."""

import pytest
from fastapi.testclient import TestClient

from tareas.adaptadores.entrada.api_fastapi import crear_app
from tareas.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from tareas.aplicacion.servicio_tareas import ServicioTareas


@pytest.fixture
def cliente() -> TestClient:
    repositorio = RepositorioSQLite(":memory:")
    return TestClient(crear_app(ServicioTareas(repositorio)))


def test_flujo_crud_completo(cliente):
    # Crear
    respuesta = cliente.post("/tareas", json={"titulo": "Aprender FastAPI"})
    assert respuesta.status_code == 201
    tarea_id = respuesta.json()["id"]

    # Leer
    assert cliente.get(f"/tareas/{tarea_id}").json()["titulo"] == "Aprender FastAPI"
    assert len(cliente.get("/tareas").json()) == 1

    # Actualizar
    respuesta = cliente.patch(f"/tareas/{tarea_id}", json={"completada": True})
    assert respuesta.json()["completada"] is True

    # Eliminar
    assert cliente.delete(f"/tareas/{tarea_id}").status_code == 204
    assert cliente.get(f"/tareas/{tarea_id}").status_code == 404


def test_titulo_vacio_devuelve_422(cliente):
    assert cliente.post("/tareas", json={"titulo": ""}).status_code == 422


def test_tarea_inexistente_devuelve_404(cliente):
    assert cliente.get("/tareas/999").status_code == 404


def test_salud(cliente):
    assert cliente.get("/salud").json() == {"estado": "ok"}
