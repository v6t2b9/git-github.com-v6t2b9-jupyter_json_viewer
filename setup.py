from setuptools import setup, find_packages

setup(
    name="jupyter_json_viewer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "ipython>=7.0.0",
    ],
    python_requires=">=3.6",
)