# Atajos para el día a día. Usa `make ayuda` para ver los comandos.
IMAGEN ?= tareas-hexagonal
MOTOR  ?= podman

.PHONY: ayuda instalar ejecutar test lint imagen contenedor

ayuda: ## Muestra esta ayuda
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

instalar: ## Instala dependencias de desarrollo
	pip install -r requirements-dev.txt

ejecutar: ## Levanta la API en http://localhost:8000/docs
	PYTHONPATH=src uvicorn tareas.principal:app --reload

test: ## Ejecuta las pruebas
	pytest

lint: ## Revisa el estilo del código
	ruff check . && ruff format --check .

imagen: ## Construye la imagen con Podman (o MOTOR=docker)
	$(MOTOR) build -t $(IMAGEN) -f Containerfile .

contenedor: imagen ## Ejecuta el contenedor en el puerto 8000
	$(MOTOR) run --rm -p 8000:8000 -v tareas-datos:/datos $(IMAGEN)
