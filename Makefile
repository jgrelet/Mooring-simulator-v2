PROJECT = MooringSimulator
MAIN = ${PROJECT}.py
PYTHON = python
PYLINT = pylint
TEST_PATH = tests

.PHONY:  clean-build clean lint test run build

clean-all:  clean-build clean

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

clean:
ifeq ($(OS),Windows_NT)
		del /Q $(PROF_DIR)
		del /Q $(SECT_DIR)
else
		rm plots/*
		rm sections/*
endif

lint:
	$(PYLINT) --exclude=.tox

test: 
	$(PYTHON) -m unittest  discover -v  $(TEST_PATH)
	
build:
	pyinstaller -wF --clean $(MAIN)

run:
	$(PYTHON) $(MAIN)
	
lib: 
	$(PYTHON) $(MAIN) --lib library\test.xls
	
runc:
	dist/$(PROJECT)
