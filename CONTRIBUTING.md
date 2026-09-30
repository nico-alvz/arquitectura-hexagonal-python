# Cómo contribuir

¡Gracias por querer mejorar este ejemplo! Es un proyecto educativo, así que la **claridad** vale más que la sofisticación.

## Preparar el entorno

```bash
python -m venv .venv && source .venv/bin/activate
make instalar
```

## Antes de abrir un Pull Request

```bash
make lint   # estilo
make test   # pruebas
```

## Convención de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/) con mensajes **en inglés**:

```
feat: add endpoint to filter tasks
fix: return 404 when task does not exist
docs: explain the ports and adapters diagram
```

## Reglas de la arquitectura

1. `dominio/` no importa nada de otras carpetas.
2. `aplicacion/` solo importa de `dominio/`.
3. `adaptadores/` pueden importar de `aplicacion/` y `dominio/`, nunca entre sí.
4. Los comentarios y la documentación se escriben en español neutro.
