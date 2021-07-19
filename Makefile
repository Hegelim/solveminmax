.PHONY: clean develop test install bdist_wheel version

develop:
	$ python setup.py develop

install:
	$ python setup.py install

test:
	$ python -m pytest

generateapi:
	$ cd docs
	$ make clean
	$ cd ..
	$ sphinx-apidoc -f -e -o docs/source/ src/solveminmax/
	$ cd docs
	$ make html
