build:
	uv run --script build_workflow.py
	uv build

test:
	uv run --no-project python -m unittest discover -s tests

generate-json:
	uv run --script rfc.py
