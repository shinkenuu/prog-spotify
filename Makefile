test:
	pytest ./tests -vv

lint:
	ruff check . --fix

clean:
	rm -r ./**/__pycache__/
	rm -r .pytest_cache/
	rm .cache