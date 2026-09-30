"""Adaptador de salida: guarda las tareas en una base de datos SQLite.

Usa solo la librería estándar de Python (`sqlite3`). Implementa exactamente el mismo
puerto que `RepositorioMemoria`, así que el resto de la aplicación no nota la diferencia.
"""

import sqlite3

from tareas.aplicacion.puertos import RepositorioTareas
from tareas.dominio.tarea import Tarea


class RepositorioSQLite(RepositorioTareas):
    def __init__(self, ruta_db: str = "tareas.db") -> None:
        # `check_same_thread=False` porque FastAPI puede atender peticiones en varios hilos.
        self._conexion = sqlite3.connect(ruta_db, check_same_thread=False)
        self._conexion.row_factory = sqlite3.Row
        self._conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS tareas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo      TEXT    NOT NULL,
                descripcion TEXT    NOT NULL DEFAULT '',
                completada  INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        self._conexion.commit()

    @staticmethod
    def _a_tarea(fila: sqlite3.Row) -> Tarea:
        """Traduce una fila de la base de datos a una entidad del dominio."""
        return Tarea(
            id=fila["id"],
            titulo=fila["titulo"],
            descripcion=fila["descripcion"],
            completada=bool(fila["completada"]),
        )

    def guardar(self, tarea: Tarea) -> Tarea:
        if tarea.id is None:
            cursor = self._conexion.execute(
                "INSERT INTO tareas (titulo, descripcion, completada) VALUES (?, ?, ?)",
                (tarea.titulo, tarea.descripcion, int(tarea.completada)),
            )
            tarea.id = cursor.lastrowid
        else:
            self._conexion.execute(
                "UPDATE tareas SET titulo = ?, descripcion = ?, completada = ? WHERE id = ?",
                (tarea.titulo, tarea.descripcion, int(tarea.completada), tarea.id),
            )
        self._conexion.commit()
        return tarea

    def obtener(self, tarea_id: int) -> Tarea | None:
        fila = self._conexion.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,)).fetchone()
        return self._a_tarea(fila) if fila else None

    def listar(self) -> list[Tarea]:
        filas = self._conexion.execute("SELECT * FROM tareas ORDER BY id").fetchall()
        return [self._a_tarea(f) for f in filas]

    def eliminar(self, tarea_id: int) -> bool:
        cursor = self._conexion.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        self._conexion.commit()
        return cursor.rowcount > 0
