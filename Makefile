# System Medic - Comandos útiles

.PHONY: help install dev prod test clean migrate superuser

help: ## Mostrar ayuda
	@echo "System Medic - Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	pip install -r requirements.txt

dev: ## Ejecutar en modo desarrollo
	python manage.py runserver

prod: ## Ejecutar en modo producción
	python manage.py collectstatic --noinput
	gunicorn crud.wsgi:application --bind 0.0.0.0:8000

test: ## Ejecutar tests
	python manage.py test

migrate: ## Crear y ejecutar migraciones
	python manage.py makemigrations
	python manage.py migrate

superuser: ## Crear superusuario
	python manage.py createsuperuser

setup: ## Configuración inicial completa
	python setup.py

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov

docker-dev: ## Ejecutar con Docker en modo desarrollo
	docker-compose -f docker-compose.dev.yml up --build

docker-prod: ## Ejecutar con Docker en modo producción
	docker-compose up --build

docker-clean: ## Limpiar contenedores Docker
	docker-compose down -v
	docker system prune -f

shell: ## Abrir shell de Django
	python manage.py shell

dbshell: ## Abrir shell de base de datos
	python manage.py dbshell

collectstatic: ## Recolectar archivos estáticos
	python manage.py collectstatic --noinput

loaddata: ## Cargar datos de ejemplo
	python manage.py loaddata fixtures/initial_data.json

dumpdata: ## Exportar datos
	python manage.py dumpdata --indent 2 > backup.json

backup: ## Crear backup de la base de datos
	python manage.py dumpdata --indent 2 > backup_$(shell date +%Y%m%d_%H%M%S).json

restore: ## Restaurar backup (especificar archivo con FILE=backup.json)
	python manage.py loaddata $(FILE)

check: ## Verificar configuración
	python manage.py check

lint: ## Ejecutar linter
	flake8 .
	black --check .

format: ## Formatear código
	black .
	isort .

coverage: ## Ejecutar tests con cobertura
	coverage run --source='.' manage.py test
	coverage report
	coverage html

docs: ## Generar documentación
	python manage.py generate_docs

security: ## Verificar seguridad
	python manage.py check --deploy
	bandit -r .

# Comandos de desarrollo
dev-install: install migrate superuser ## Instalación completa para desarrollo

dev-reset: clean migrate superuser ## Resetear base de datos y crear superusuario

# Comandos de Docker
docker-build: ## Construir imagen Docker
	docker build -t system-medic .

docker-run: ## Ejecutar contenedor Docker
	docker run -p 8000:8000 system-medic

# Comandos de base de datos
db-reset: ## Resetear base de datos
	rm -f db.sqlite3
	python manage.py migrate
	python manage.py createsuperuser

db-backup: ## Backup de base de datos
	cp db.sqlite3 backup_$(shell date +%Y%m%d_%H%M%S).sqlite3

# Comandos de traducción
makemessages: ## Crear archivos de traducción
	python manage.py makemessages -l es
	python manage.py makemessages -l en
	python manage.py makemessages -l pt

compilemessages: ## Compilar traducciones
	python manage.py compilemessages

# Comandos de logs
logs: ## Ver logs en tiempo real
	tail -f logs/django.log

# Comandos de monitoreo
status: ## Ver estado del sistema
	@echo "=== Estado del Sistema ==="
	@echo "Python: $(shell python --version)"
	@echo "Django: $(shell python -c 'import django; print(django.get_version())')"
	@echo "Base de datos: $(shell python manage.py dbshell -c 'SELECT sqlite_version();' 2>/dev/null || echo 'PostgreSQL')"
	@echo "Archivos estáticos: $(shell ls -la static/ | wc -l) archivos"
	@echo "Plantillas: $(shell find templates/ -name '*.html' | wc -l) archivos"
