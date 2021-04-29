PROJECT = MooringSimulator
MAIN = ${PROJECT}.py
PYTHON = python
PYLINT = pylint
TEST_PATH = tests

.PHONY:  clean-build lint test run build

clean-all:  clean-build

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	
clean-build:
ifeq ($(OS),Windows_NT) 
		del /Q build dist __pycache__
else
		rm --force --recursive build/
		rm --force --recursive dist/
		rm --force --recursive __pycache__/
endif

lint:
	$(PYLINT) $(MAIN)

test: 
	$(PYTHON) -m unittest  discover -v  $(TEST_PATH)
	
build:
	pyinstaller -wF -c --clean $(MAIN)

run:
	$(PYTHON) $(MAIN)
	
lib: 
	$(PYTHON) $(MAIN) --lib library\test.xls
	
runc:
	dist/$(PROJECT)
