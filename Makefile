.PHONY: clean develop test install bdist_wheel version

develop:
	$ python setup.py develop

install:
	$ python setup.py install

test:
	$ python -m pytest

generateapi:
	$(MAKE) -C docs clean; \
	$ sphinx-apidoc -fo docs/source/ src/; \
	$(MAKE) -C docs html; \

updateyaml
	$ git add .readthedocs.yaml; \
	$ git commit -m "Update .readthedocs.yaml"; \
	$ git push
