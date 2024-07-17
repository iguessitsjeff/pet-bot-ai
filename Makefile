SOURCE=src
PIPENV=pipenv
PIPENV_VENV_IN_PROJECT=1

.PHONY: install
install:
	export PIPENV_VENV_IN_PROJECT=${PIPENV_VENV_IN_PROJECT}; \
	$(PIPENV) install --dev

.PHONY: invoke-event
invoke-event:
	$(PIPENV) requirements > requirements.txt; \
	sam build --manifest requirements.txt; \
	sam local invoke --event sns_event.json

.PHONY: linter
linter:
	$(PIPENV) run ruff check

.PHONY: formatter
formatter:
	$(PIPENV) run ruff check --fix
	$(PIPENV) run ruff format
