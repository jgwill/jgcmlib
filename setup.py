from setuptools import setup, find_packages

setup(
    name='jgcmlib',
    version='1.0.0',
    author='J.Guillaume D-Isabelle',
    description='A Python module jgcmlib',
    packages=find_packages(),
    install_requires=[
        "tlid",
        "requests"
    ],
    entry_points={
        'console_scripts': [
            # Add any console scripts or entry points here
        ]
    },
)