test:
	uv run pytest ./tests -vv

lint:
	uv tool run ruff check . --fix

clean:
	rm -r ./**/__pycache__/
	rm -r .pytest_cache/
	rm .cache

# CLI shortcuts
catch-up:
	uv run progspot catch-up

.PHONY: test lint clean catch-up
