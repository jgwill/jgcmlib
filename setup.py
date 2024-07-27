from setuptools import setup, find_packages

setup(
    name='jgcmlib',
    version='1.0.19',
    author='J.Guillaume D-Isabelle',
    description='A Python module jgcmlib',
    url='https://github.com/jgwill/jgcmlib',
    packages=find_packages(),
    install_requires=[
        "tlid",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            "jgabcli = jgcmlib.jgabcli:main"
        ]
    },
)