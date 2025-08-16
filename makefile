freeze:
	uv pip freeze > requirements.txt

install-req:
	uv pip install -r requirements.txt

run:
	uv run main.py