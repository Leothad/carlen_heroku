clean:
	rm -rf build dist src/*.egg-info .tox .pytest_cache pip-wheel-metadata .DS_Store
	find src -name '__pycache__' | xargs rm -rf
	find tests -name '__pycache__' | xargs rm -rf

dev:
	python -m pip install -e .[dev]

install:
	python -m pip install -e .

run:
	FLASK_DEBUG=true FLASK_APP=carlen flask run

.PHONY: all clean dev install