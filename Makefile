migration:
	alembic revision --autogenerate -m "$(m)"

migrate:
	alembic upgrade head

migrate_rollback:
	alembic downgrade -1

migrate_history:
	alembic history

start:
    uvicorn app.main:app --reload