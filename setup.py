# -*- coding: utf-8 -*-

"""
A timing library providing timer functionality.
"""

import os.path
from setuptools import setup, find_packages


def read(*path_elements: str, **kwargs: str) -> str:
    """ Read file contents. """
    path = os.path.join(os.path.dirname(__file__), *path_elements)
    encoding = kwargs.pop('encoding', 'utf-8')
    with open(path, encoding=encoding, **kwargs) as fp:
        return fp.read().strip()


setup(
    name="timing",
    version=read("VERSION"),
    description="The only timing library you'll ever need.",
    long_description="README.md",
    author="ruzickbelle",
    url="https://github.com/ruzickbelle/python-timing",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    license=read("LICENSE"),
    keywords=["timer", "timing"],
    install_requires=[],
    extras_require={"dev": [
        "autopep8",
        "pylint",
        "pytest",
    ]},
    packages=find_packages("src"),
    package_dir={'': "src"},
    python_requires=">=3.0",
)
