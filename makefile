PYTHON_TESTS = $(wildcard test*.py)

check: $(PYTHON_TESTS) 
	python -m unittest $(PYTHON_TESTS)

$(PYTHON_TESTS):


.PHONY: all clean check $(PYTHON_TESTS)

