import runpy

from setuptools import setup

# Ref : https://packaging.python.org/single_source_version/#single-sourcing-the-version
# runpy is safer and a better habit than exec
version = runpy.run_path("datacrystals/_version.py")
__version__ = version.get("__version__")

setup(
    name="datacrystals",
    version=__version__,
    description="datacrystals",
    url="http://github.com/asmodehn/datacrystals",
    author="AlexV",
    author_email="asmodehn@gmail.com",
    license="GPLv3",
    packages=["datacrystals"],
    install_requires=[
        "pandas",
        "hypothesis",
        "tabulate",
    ],
    zip_safe=False,
)
