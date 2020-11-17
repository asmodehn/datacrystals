from setuptools import setup

setup(
    name="datacrystals",
    version="0.1",
    description="datacrystals",
    url="http://github.com/asmodehn/datacrystals",
    author="AlexV",
    author_email="asmodehn@gmail.com",
    license="GPLv3",
    packages=["datacrystals"],
    install_requires=[
        "pydantic",
        "pandas",
        "hypothesis",
        "tabulate",
    ],
    zip_safe=False,
)
