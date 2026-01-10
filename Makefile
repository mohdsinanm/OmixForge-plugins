PYTHON := poetry run python

.PHONY : check 

check:
	$(PYTHON) check_plugins.py

