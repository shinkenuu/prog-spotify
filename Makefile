test:
	pytest ./tests -vv

clean:
	rm -r ./**/__pycache__/
	rm -r .pytest_cache/
	rm .cache