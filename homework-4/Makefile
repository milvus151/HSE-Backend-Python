PIP := venv/Scripts/pip.exe
PYTHON := venv/Scripts/python.exe
TESTS := venv/Scripts/pytest.exe -v test_controllers.py

clear:
	rmdir /S /Q venv

venv:
	python -m venv venv

install_requirements:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) server.py

test:
	$(TESTS)

