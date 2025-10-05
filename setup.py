from setuptools import setup, find_packages
import setuptools


VERSION = "1.0"
DESCRIPTION = "Vinted Python client"

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="vinted-wardrobe-refresher",
    version=VERSION,
    author="Paolo Compieta",
    author_email="paolocompieta@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=["requests"],
    keywords=["python", "Vinted", "export", "wardrobe", "scrape"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Education",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.13",
    url="https://github.com/pcompieta/vinted-wardrobe-refresher",
)
