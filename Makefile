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

.PHONY: bump_version
bump_version:
	python bump_version.py
	git commit . -m "Bump version"

.PHONY: release
release:
	make bump_version
	make dist
	git tag  $(version) -m "Release version $(version)"
	git push origin $(version)
	make pypi-release

.PHONY: tstv
tstv:
	version2=$(shell python bump_version.py)
	echo "version: $(version)"