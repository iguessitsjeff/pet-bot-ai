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
	sam local invoke --profile $(aws_profile) --event sns_event.json

.PHONEY: start_api
start_api:
	$(PIPENV) requirements > requirements.txt; \
	sam build --manifest requirements.txt; \
	sam local start-api --profile $(aws_profile) --parameter-overrides 'ApplicationEnv=dev'

.PHONY: linter
linter:
	$(PIPENV) run ruff check

.PHONY: formatter
formatter:
	$(PIPENV) run ruff check --fix
	$(PIPENV) run ruff format
