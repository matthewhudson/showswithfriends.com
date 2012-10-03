VIRTUALENV_PATH = venv
VIRTUALENV_BIN = $(VIRTUALENV_PATH)/bin

DEV_ENV = source $(VIRTUALENV_BIN)/activate ;
PIP = $(VIRTUALENV_BIN)/pip
PYTHON = $(ENV) $(VIRTUALENV_BIN)/python

.PHONY: venv
venv:
	virtualenv --distribute $(VIRTUALENV_PATH)
	$(PIP) install -r requirements.txt

.PHONY: server
server:
	$(PYTHON) runserver.py
