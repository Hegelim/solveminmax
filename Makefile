.PHONY: clean develop test install bdist_wheel version

develop:
	$ python setup.py develop

install:
	$ python setup.py install

test:
	$ python -m pytest

