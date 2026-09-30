"""Adaptador de entrada: línea de comandos.

Demuestra que el mismo `ServicioTareas` se puede usar desde otra "puerta" distinta de
HTTP sin cambiar el núcleo. Recibe el servicio ya armado, igual que la API.
"""

import argparse

from tareas.aplicacion.servicio_tareas import ServicioTareas
from tareas.dominio.errores import ErrorDeDominio


def _crear_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tareas", description="Gestor de tareas")
    sub = parser.add_subparsers(dest="comando", required=True)
    crear = sub.add_parser("crear", help="Crea una tarea")
    crear.add_argument("titulo")
    sub.add_parser("listar", help="Lista las tareas")
    completar = sub.add_parser("completar", help="Marca una tarea como completada")
    completar.add_argument("id", type=int)
    eliminar = sub.add_parser("eliminar", help="Elimina una tarea")
    eliminar.add_argument("id", type=int)
    return parser


def ejecutar(servicio: ServicioTareas, argumentos: list[str]) -> int:
    """Ejecuta un comando y devuelve el código de salida (0 = éxito)."""
    args = _crear_parser().parse_args(argumentos)
    try:
        if args.comando == "crear":
            tarea = servicio.crear(args.titulo)
            print(f"Creada #{tarea.id}: {tarea.titulo}")
        elif args.comando == "listar":
            for t in servicio.listar():
                print(f"[{'x' if t.completada else ' '}] #{t.id} {t.titulo}")
        elif args.comando == "completar":
            servicio.actualizar(args.id, completada=True)
        elif args.comando == "eliminar":
            servicio.eliminar(args.id)
    except ErrorDeDominio as error:
        print(f"Error: {error}")
        return 1
    return 0
