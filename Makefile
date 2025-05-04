.DEFAULT_GOAL := about
VERSION := $(shell cat pybmoore/__init__.py | grep '__version__ =' | cut -d'"' -f 2)
USE_CYTHON := false

lint:
ifeq ($(SKIP_STYLE), )
	@echo "> running isort..."
	isort setup.py
	isort pybmoore
	isort tests
	@echo "> running black..."
	black setup.py
	black pybmoore
	black tests
endif
	@echo "> running bandit"
	bandit -r -ll -ii -s B104 pybmoore
	@echo "> running radon"
	radon cc -s -n B pybmoore tests
	@echo "> running flake8..."
	flake8 setup.py
	flake8 pybmoore
	flake8 tests
	@echo "> running mypy..."
	mypy pybmoore

tests:
	@echo "> unittest"
	python -m pytest --durations=10 -vv --no-cov-on-fail --color=yes --cov-report xml --cov-report term --cov=pybmoore tests

ci: lint tests
ifeq ($(GITHUB_HEAD_REF), false)
	@echo "> uploading coverage report..."
	codecov -f coverage.xml -t $$CODECOV_TOKEN
endif

build:
	@echo "> building package..."
	python setup.py build_ext -i
	python setup.py sdist
	@echo "OK"

clean:
	@echo "> cleaning up the environment"
	@rm pybmoore/_bm.c | true
	@rm pybmoore/*.so | true
	@rm pybmoore/*.html | true
	@rm dist/*.tar.gz | true
ifeq ($(FORCE), true)
	@rm pybmoore/_bm.c | true
endif
	@echo "OK"

about:
	@echo "> pybmoore [$(VERSION)]"
	@echo ""
	@echo "make lint   - Runs: [isort > black > flake8 > mypy]"
	@echo "make tests  - Runs: [tests]"
	@echo "make ci     - Runs: [lint > tests]"
	@echo "make clean  - Clean the environment for a new build [flag available, default FORCE=false]."
	@echo "make build  - Build package [flag available, default USE_CYTHON=false]."
	@echo ""
	@echo "mailto: alexandre.fmenezes@gmail.com"

all: build ci

.PHONY: lint tests ci clean build all
