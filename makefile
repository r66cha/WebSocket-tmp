freeze:
	uv pip freeze > requirements.txt

install-req:
	uv pip install -r requirements.txt

run-server:
	uv run main.py

run-client:
	uv run src/api/client/ws_client.py