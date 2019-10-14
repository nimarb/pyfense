# How to Publish the Game and Turn It Into a Python Package

1. go to the top level folder (pyfense is a sub folder in that one)
2. check the version number in setup.py
3. the version number has to be increased with every build
4. to build the package run: `python setup.py sdist`
5. if you want to build and upload to pypi, run: `python setup.py sdist upload` (that step requires a pypi account with saved credentials)

basic getting started guide: https://jamie.curle.io/posts/my-first-experience-adding-package-pypi/
