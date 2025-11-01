from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cflpr",
    packages=["cflpr"],
    version="0.0.1",
    license="MIT",
    description="A simple Python library for accessing CFL P+R APIs (https://www.cfl.lu/fr-fr/app/parkandride)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="adetante",
    url="https://github.com/adetante/python-cflpr",
    keywords=[
        "CFL",
        "P+R",
        "PARKING",
    ],
    install_requires=["aiohttp>=3.12.1"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.13",
    ],
)
