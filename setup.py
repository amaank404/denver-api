import setuptools
from denverapi import pysetup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="denver_api",
    packages=setuptools.find_packages()+setuptools.find_namespace_packages(include=["denverapi", "denverapi.*"]),
    package_data=pysetup.find_package_data("denverapi", "denverapi"),
    version="2.2.2",
    author="xcodz",
    description="Denver API for python full-stack development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "requests",
        "playsound",
        "pygame",
        "cryptography"
    ],
    zip_safe=False
)
