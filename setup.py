from setuptools import setup
import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="litex-modules",
    version="v0.0.1",
    author="David Jablonski",
    author_email="dayjaby@gmail.com",
    description="LiteX modules",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/dayjaby/litex-modules",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
    ]
)
