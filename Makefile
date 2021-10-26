.DEFAULT_GOAL := about
VERSION := $(shell cat pybmoore/__version__.py | cut -d'"' -f 2)
USE_CYTHON := 1

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort setup.py
	isort pybmoore/
	isort tests/
	@echo "> running black..."
	black setup.py
	black pybmoore
	black tests
endif
	@echo "> running flake8..."
	flake8 setup.py
	flake8 pybmoore
	flake8 tests
	@echo "> running mypy..."
	mypy pybmoore

tests:
	@echo "> unittest"
	python -m pytest --durations=5 -vv --no-cov-on-fail --color=yes --cov-report xml --cov-report term --cov=pybmoore tests

install-deps:
	@echo "> installing dependencies..."
	pip install -r requirements-dev.txt

tox:
	@echo "> running tox..."
	tox -r -p all

build:
	@echo "> building package..."
	python setup.py build_ext -i
	python setup.py sdist bdist_wheel

clean:
	@echo "> cleaning up the environment"
	rm pybmoore/*.so
	rm pybmoore/*.html

publish: build
	TWINE_PASSWORD=${CI_JOB_TOKEN} TWINE_USERNAME=gitlab-ci-token python -m twine upload --repository-url https://gitlab.com/api/v4/projects/${CI_PROJECT_ID}/packages/pypi dist/*


about:
	@echo "> pybmoore [$(VERSION)]"
	@echo ""
	@echo "make lint         - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests        - Run: tests."
	@echo "make ci           - Runs: [lint > tests]"
	@echo "make tox          - Runs tox."
	@echo "make build        - Build package."
	@echo "make install-deps - Install development dependencies."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "> download CI dependencies"
	curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
	chmod +x ./cc-test-reporter
	@echo "> uploading report..."
	codecov --file coverage.xml -t $$CODECOV_TOKEN
	./cc-test-reporter format-coverage -t coverage.py -o codeclimate.json
	./cc-test-reporter upload-coverage -i codeclimate.json -r $$CC_TEST_REPORTER_ID
endif

all: install-deps ci build

.PHONY: lint tests ci tox build install-deps clean all
