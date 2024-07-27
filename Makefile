version := $(shell python setup.py --version)

.PHONY: clean
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -f
	rm -Rf dist
	rm -Rf *.egg-info

.PHONY: authors
authors:
	git log --format='%aN <%aE>' `git describe --abbrev=0 --tags`..@ | sort | uniq >> AUTHORS
	cat AUTHORS | sort --ignore-case | uniq >> AUTHORS_
	mv AUTHORS_ AUTHORS

.PHONY: dist
dist:
	make clean
	python -m build

.PHONY: pypi-release
pypi-release:
	twine --version
	twine upload -s dist/*

.PHONY: release
release:
	version=$(shell python bump_version.py)
    # Display the new version
    echo "New version: $(version)"
    make dist
	git tag -s $(version) -m "Release version $(version)"
	git push origin $(version)
	make pypi-release

.PHONY: tstv
tstv:
	echo "version: $(version)"
