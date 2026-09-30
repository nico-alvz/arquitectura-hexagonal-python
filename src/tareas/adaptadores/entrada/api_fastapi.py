"""Adaptador de entrada: expone los casos de uso como una API REST con FastAPI.

Su única responsabilidad es traducir: HTTP -> llamada al servicio -> respuesta HTTP.
No contiene reglas de negocio.
"""

from fastapi import APIRouter, FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from tareas.aplicacion.servicio_tareas import ServicioTareas
from tareas.dominio.errores import TareaNoEncontrada, TituloInvalido
from tareas.dominio.tarea import Tarea


# --- Modelos HTTP (lo que viaja por la red; distintos de la entidad del dominio) ---
class TareaEntrada(BaseModel):
    titulo: str
    descripcion: str = ""


class TareaActualizacion(BaseModel):
    titulo: str | None = None
    descripcion: str | None = None
    completada: bool | None = None


class TareaSalida(BaseModel):
    id: int
    titulo: str
    descripcion: str
    completada: bool = Field(description="`true` si la tarea ya fue terminada")

    @classmethod
    def desde_dominio(cls, tarea: Tarea) -> "TareaSalida":
        return cls(
            id=tarea.id,
            titulo=tarea.titulo,
            descripcion=tarea.descripcion,
            completada=tarea.completada,
        )


def crear_app(servicio: ServicioTareas) -> FastAPI:
    """Construye la aplicación FastAPI recibiendo el servicio ya armado."""
    app = FastAPI(title="Tareas — Arquitectura Hexagonal", version="1.0.0")
    router = APIRouter(prefix="/tareas", tags=["tareas"])

    # Traducción de errores del dominio a códigos HTTP.
    @app.exception_handler(TareaNoEncontrada)
    def _no_encontrada(_, error: TareaNoEncontrada):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(error)})

    @app.exception_handler(TituloInvalido)
    def _titulo_invalido(_, error: TituloInvalido):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content={"detail": str(error)}
        )

    @router.post("", response_model=TareaSalida, status_code=status.HTTP_201_CREATED)
    def crear(datos: TareaEntrada):
        return TareaSalida.desde_dominio(servicio.crear(datos.titulo, datos.descripcion))

    @router.get("", response_model=list[TareaSalida])
    def listar():
        return [TareaSalida.desde_dominio(t) for t in servicio.listar()]

    @router.get("/{tarea_id}", response_model=TareaSalida)
    def obtener(tarea_id: int):
        return TareaSalida.desde_dominio(servicio.obtener(tarea_id))

    @router.patch("/{tarea_id}", response_model=TareaSalida)
    def actualizar(tarea_id: int, datos: TareaActualizacion):
        tarea = servicio.actualizar(tarea_id, **datos.model_dump())
        return TareaSalida.desde_dominio(tarea)

    @router.delete("/{tarea_id}", status_code=status.HTTP_204_NO_CONTENT)
    def eliminar(tarea_id: int):
        servicio.eliminar(tarea_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @app.get("/salud", tags=["salud"])
    def salud():
        return {"estado": "ok"}

    app.include_router(router)
    return app
