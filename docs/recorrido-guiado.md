# Recorrido guiado: una tarea a través de la arquitectura

Esta práctica conecta las piezas del código con resultados observables. Ejecuta los comandos desde la raíz del repositorio y prepara el entorno de Python según el [README](../README.md#-inicio-rápido).

## 1. Ejecutar un caso de uso sin servidor

El siguiente ejemplo conecta manualmente el servicio con dos adaptadores en memoria. No necesita FastAPI ni archivos de datos.

```bash
PYTHONPATH=src python - <<'PY'
from tareas.adaptadores.salida.notificador_memoria import NotificadorMemoria
from tareas.adaptadores.salida.repositorio_memoria import RepositorioMemoria
from tareas.aplicacion.servicio_tareas import ServicioTareas
from tareas.dominio.errores import TituloInvalido

notificador = NotificadorMemoria()
servicio = ServicioTareas(RepositorioMemoria(), notificador)
tarea = servicio.crear("Seguir el recorrido de una tarea")
assert tarea.id == 1
assert tarea.completada is False

servicio.actualizar(tarea.id, completada=True)
servicio.actualizar(tarea.id, completada=True)
assert len(notificador.completadas) == 1

try:
    servicio.crear("   ")
except TituloInvalido as error:
    print(error)
else:
    raise AssertionError("El dominio debe rechazar un título vacío")

print(f"Tareas: {len(servicio.listar())}; avisos: {len(notificador.completadas)}")
PY
```

Resultado esperado:

```text
El título no puede estar vacío
Tareas: 1; avisos: 1
```

Lee el constructor de [`ServicioTareas`](../src/tareas/aplicacion/servicio_tareas.py): recibe los colaboradores que necesita. Este script hace el trabajo de composición que, en la aplicación, realiza [`composicion.py`](../src/tareas/composicion.py).

El ejemplo importa adaptadores porque los conecta. El servicio solo importa sus contratos; esa diferencia permite probarlo con distintas implementaciones.

## 2. Conservar datos entre comandos

La CLI crea un proceso por comando. Usa JSON para observar que los datos sobreviven entre ejecuciones. Este bloque utiliza un directorio temporal nuevo para que el primer identificador sea `1`.

```bash
(
    export PYTHONPATH=src
    export REPOSITORIO=json
    export RUTA_JSON="$(mktemp -d)/tareas.json"

    python -m tareas.principal_cli crear "Leer los puertos"
    python -m tareas.principal_cli listar
    python -m tareas.principal_cli completar 1
    python -m tareas.principal_cli listar
    python -m tareas.principal_cli eliminar 1
    python -m tareas.principal_cli listar
)
```

Observa estos cambios:

1. La creación muestra `Creada #1: Leer los puertos`.
2. La primera lista contiene `[ ] #1 Leer los puertos`.
3. Completar genera un aviso del notificador de consola.
4. La segunda lista contiene `[x] #1 Leer los puertos`.
5. Después de eliminar, la lista no imprime tareas.

Los paréntesis limitan las variables a esta práctica. El archivo queda en el directorio temporal generado. Si cambias `json` por `memoria`, la primera tarea desaparece al terminar el comando `crear`: el siguiente proceso construye otro repositorio vacío.

## 3. Seguir una petición HTTP

Inicia la API con `make ejecutar` y crea una tarea desde `/docs` o con los ejemplos del README. Sigue estas llamadas en el código:

| Paso | Archivo | Qué ocurre |
|---|---|---|
| 1 | [`api_fastapi.py`](../src/tareas/adaptadores/entrada/api_fastapi.py) | FastAPI interpreta el JSON como `TareaEntrada` y llama a `servicio.crear` |
| 2 | [`servicio_tareas.py`](../src/tareas/aplicacion/servicio_tareas.py) | El servicio construye una `Tarea` |
| 3 | [`tarea.py`](../src/tareas/dominio/tarea.py) | La entidad valida que el título tenga contenido y hasta 100 caracteres |
| 4 | [`puertos.py`](../src/tareas/aplicacion/puertos.py) | El contrato establece la operación `guardar` que usa el servicio |
| 5 | [`repositorio_sqlite.py`](../src/tareas/adaptadores/salida/repositorio_sqlite.py) | El adaptador predeterminado guarda la tarea y asigna su identificador |
| 6 | [`api_fastapi.py`](../src/tareas/adaptadores/entrada/api_fastapi.py) | Convierte la entidad a `TareaSalida` y devuelve `201` |

El paso 4 representa el contrato, no una capa adicional que procese la petición: la llamada se ejecuta sobre el adaptador inyectado. Si falla la regla del título, no se llega a guardar la tarea.

Prueba también un JSON sin `titulo`: FastAPI lo rechaza al validar la entrada. Luego prueba `{"titulo":"   "}`: tiene el campo requerido, pero viola una regla del dominio. Ambos producen `422` por caminos distintos.

## 4. Ejercicios para modificar el proyecto

Antes de editar, anticipa qué archivos deberían cambiar. Después, comprueba esa predicción con el diff y las pruebas.

| Ejercicio | Dónde empezar | Cómo comprobarlo |
|---|---|---|
| Cambiar SQLite por JSON | `REPOSITORIO=json make ejecutar` | Crea una tarea, reinicia la API con la misma configuración y verifica que sigue disponible; no necesitas editar el servicio |
| Agregar `listar_pendientes` | `ServicioTareas`, filtrando `repositorio.listar()` | Crea una tarea pendiente y otra completada: el nuevo método debe devolver solo la pendiente; conserva las pruebas existentes |
| Exponer el nuevo caso de uso en la CLI | `cli.py`, agregando un subcomando | Verifica que el comando llama al servicio y muestra solo las pendientes, sin repetir el filtro en el adaptador |
| Implementar otro repositorio | Un adaptador de salida y `composicion.py` | Añádelo a la fixture parametrizada de `test_contrato_repositorio.py` y ejecuta la misma batería para todas las implementaciones |

Para el ejercicio de pendientes, el contrato actual ya permite listar todas las tareas. Si más adelante necesitas que el almacenamiento haga el filtrado, amplía el puerto y actualiza todas sus implementaciones.

```bash
python -m pytest tests/test_servicio_tareas.py tests/test_notificador.py
python -m pytest tests/test_contrato_repositorio.py
make lint
make test
```

Las pruebas de contrato comprueban comportamientos comunes; no garantizan por sí solas que todos los repositorios tengan las mismas propiedades operativas. Por ejemplo, JSON lee y reescribe el archivo completo y no coordina escrituras concurrentes. El notificador de consola tampoco implementa entrega persistente ni reintentos.

## Preguntas de comprobación

- **¿Dónde se decide usar SQLite?** En `composicion.py`, al construir los colaboradores del servicio.
- **¿Por qué el dominio no devuelve un HTTP 422?** Porque también se usa desde la CLI; cada entrada traduce el mismo error a su propio formato.
- **¿Hace falta una clase abstracta para cada entrada?** En este ejemplo, los métodos públicos del servicio son el puerto de entrada; API y CLI los invocan directamente.
- **¿Completar dos veces genera dos avisos?** No si la tarea ya estaba completada. El servicio notifica cada transición de pendiente a completada.

Continúa con la [guía para extender la aplicación](como-extender.md) para implementar nuevos puertos y adaptadores.
