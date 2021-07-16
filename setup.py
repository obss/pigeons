import io
import os
import re

import setuptools


def get_requirements():
    with open("requirements.txt", "r") as f:
        return list(f.read().splitlines())


def get_description(long=False):
    if long:
        with open("README.md", "r") as fh:
            description = fh.read()
    else:
        description = "Handy logging tool to send logs to MSTeams with or without filters."
    return description


def get_version():
    current_dir = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(current_dir, "pigeons", "__init__.py")
    with io.open(version_file, encoding="utf-8") as f:
        return re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', f.read(), re.M).group(1)


URL = "https://github.com/obss/pigeons"

setuptools.setup(
    name="pigeons",
    version=get_version(),
    author="",
    license="MIT",
    description=get_description(),
    long_description=get_description(long=True),
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=get_requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
