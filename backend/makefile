run:
	uvicorn app.main:app --reload


migration:
	alembic revision --autogenerate -m "$(m)"


migrate:
	alembic upgrade head