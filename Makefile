
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
    VERSION=$$(python setup.py --version)
	make dist
    git tag -s $${VERSION} -m "Release version $${VERSION}"
    git push origin $${VERSION}
	make pypi-release

