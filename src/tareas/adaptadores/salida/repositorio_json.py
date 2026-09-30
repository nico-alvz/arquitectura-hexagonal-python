"""Adaptador de salida: guarda las tareas en un archivo JSON.

Es el ejemplo de la guía `docs/como-extender.md`: un tercer repositorio que implementa
el mismo puerto. Basta con cumplir el contrato de `RepositorioTareas`.
"""

import json
from pathlib import Path

from tareas.aplicacion.puertos import RepositorioTareas
from tareas.dominio.tarea import Tarea


class RepositorioJSON(RepositorioTareas):
    def __init__(self, ruta: str | Path = "tareas.json") -> None:
        self._ruta = Path(ruta)

    def _leer(self) -> dict:
        if not self._ruta.exists():
            return {"siguiente_id": 1, "tareas": {}}
        return json.loads(self._ruta.read_text(encoding="utf-8"))

    def _escribir(self, datos: dict) -> None:
        self._ruta.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")

    def guardar(self, tarea: Tarea) -> Tarea:
        datos = self._leer()
        if tarea.id is None:
            tarea.id = datos["siguiente_id"]
            datos["siguiente_id"] += 1
        datos["tareas"][str(tarea.id)] = {
            "titulo": tarea.titulo,
            "descripcion": tarea.descripcion,
            "completada": tarea.completada,
        }
        self._escribir(datos)
        return tarea

    def obtener(self, tarea_id: int) -> Tarea | None:
        campos = self._leer()["tareas"].get(str(tarea_id))
        return Tarea(id=tarea_id, **campos) if campos else None

    def listar(self) -> list[Tarea]:
        tareas = self._leer()["tareas"]
        return [Tarea(id=int(i), **tareas[i]) for i in sorted(tareas, key=int)]

    def eliminar(self, tarea_id: int) -> bool:
        datos = self._leer()
        existia = datos["tareas"].pop(str(tarea_id), None) is not None
        if existia:
            self._escribir(datos)
        return existia
