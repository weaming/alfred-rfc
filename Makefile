.PHONY: test build install publish generate-json

# the library name
name = alfred-rfc
# may change to pip3 or python3 -m pip, etc.
pip = pip

install: clean build
	$(pip) install --force-reinstall ./dist/*.whl

build: generate-json
	python setup.py sdist
	python setup.py bdist_wheel --universal

publish: clean build
	twine upload dist/* && git push --follow-tags

uninstall:
	$(pip) uninstall $(name)

clean:
	rm -fr build dist *.egg-info

generate-json:
	python rfc.py
