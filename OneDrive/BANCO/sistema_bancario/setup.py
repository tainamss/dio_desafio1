from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="meu_pacote_banco",
    version="0.0.1",
    author="Tainá",
    author_email="taina.mesquita06@gmail.com",
    description="Um sistema bancário simples em Python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)