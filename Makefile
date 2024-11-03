local:
	uvicorn app.main:app --reload

daemon:
	python3 ./widgets/update.py
