.PHONY: help
help:
	@echo "Please use \`make <target>' where <target> is one of:"
	@echo "  init       to initialize a dev environment"
	@echo "  clean      clear tox environments and builds"
	@echo "  update-deps  recompile pip requirements"
	@echo "  update     run update-deps then init"

.PHONY: init
init:
	pip install -U tox pre-commit
	rm -rf .tox
	pre-commit install

.PHONY: clean
clean:
	rm -rf _build/*
	rm -rf .tox

.PHONY: update-deps
update-deps:
	# The pip pin is temporary, for a pip-tools incompatibility
	pip install --upgrade pip-tools "pip<22" setuptools
	pip-compile --upgrade --build-isolation --output-file requirements.txt requirements.in

update: update-deps init
