test:
	uv run pytest ./tests -vv

lint:
	uv tool run ruff check . --fix

clean:
	rm -r ./**/__pycache__/
	rm -r .pytest_cache/
	rm .cache