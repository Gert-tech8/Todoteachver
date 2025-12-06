migration:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head

migrate_rollback:
	alembic downgrade -1

migrate_history:
	alembic history

start:
    uvicorn app.main:app --host 0.0.0.0 --port 8080