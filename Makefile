install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

project:
	poetry run project

env-activate:
	poetry env activate

package-install:
	python3 -m pip install dist/*.whl