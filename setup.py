## setup.py

from setuptools import setup, find_packages

setup(
    name="jupyter-json-viewer",
    version="0.1.0",
    description="An enhanced JSON visualization tool for Jupyter Notebooks with visual hierarchy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="v6t2b9",
    author_email="v6t2b9@gmail.com",
    url="https://github.com/YourUsername/jupyter-json-viewer",
    packages=find_packages(),
    install_requires=[
        "ipython>=7.0.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
