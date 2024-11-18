#!make
# Setup the shell and python version.
# It's necessary to set this because some environments don't link sh -> bash.
SHELL := /bin/bash
PYTHON := python3.11
SERVICES := app
PY_CONFIG := app.config  # Путь до файла настроек сервиса
MESSAGE ?="auto"

DB_HOST := $(shell python -c 'from ${PY_CONFIG} import settings; print(settings.POSTGRES.host)')
DB_PORT := $(shell python -c 'from ${PY_CONFIG} import settings; print(settings.POSTGRES.port)')
DB_USER := $(shell python -c 'from ${PY_CONFIG} import settings; print(settings.POSTGRES.user)')
DB_NAME := $(shell python -c 'from ${PY_CONFIG} import settings; print(settings.POSTGRES.database)')
PG_PASSWORD := $(shell python -c 'from ${PY_CONFIG} import settings; print(settings.POSTGRES.password)')

.PHONY: help venv sort lint black migrations migrate create_db drop_db recreate_db

help:
	@echo "Использование: make <command>"
	@echo
	@echo "Доступные команды:"
	@echo "  venv                             Создание виртуального окружения"
	@echo "  sort                     		  Сортировка импортов"
	@echo "  lint                     		  Запуск линтеров"
	@echo "  black                    		  Запуск форматтера black"
	@echo "  migrations               		  Создание и добавление в индекс файла миграции"
	@echo "  migrate                  		  Обновление миграций базы данных"
	@echo "  create_db                		  Создание базы данных"
	@echo "  drop_db                  		  Удаление базы данных"
	@echo "  recreate_db                      Пересоздание базы данных"

venv:
	@$(PYTHON) -m venv .venv
	@echo "Для активации venv используйте 'source .venv/bin/activate'"

sort:
	@isort .

lint:
	@flake8 --max-line-length 120 $(SERVICES)
	@pylint $(SERVICES)

black:
	@black .

migrations:
	@alembic revision --autogenerate -m "$(shell date +'%Y-%m-%d_%H-%M-%S')-${MESSAGE}"
	@git add ./migrations/versions/.

migrate:
	@alembic upgrade head

create_db:
	@psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -c "CREATE DATABASE ${DB_NAME}"
    # Устанавливаем расширение
    # postgis - расширение для работы с геометриями, геоданными
	@psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USER} -d ${DB_NAME} -c "CREATE EXTENSION postgis;"

drop_db:
	@psql -h ${DB_HOST}	-p ${DB_PORT} -U "${DB_USER}" -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '${DB_NAME}' AND pid <> pg_backend_pid();"
	@psql -h "${DB_HOST}" -p ${DB_PORT} -U "${DB_USER}" -c "DROP DATABASE IF EXISTS ${DB_NAME};"

recreate_db:
	@PGPASSWORD=${PG_PASSWORD} make drop_db
	@PGPASSWORD=${PG_PASSWORD} make create_db
	@make migrate

format:
	@$(foreach dir,$(TARGET_DIRS),poetry run black $(dir);)
	@$(foreach dir,$(TARGET_DIRS),poetry run isort $(dir);)
