import setuptools
from denver import pysetup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="pydenver_pios_sdk",
    packages=setuptools.find_packages(include=["denver.*"])+setuptools.find_namespace_packages(include=["denver.*"]),
    package_data=pysetup.find_package_data("denver", "denver"),
    version="0.1",
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
        "pydenver"
    ],
    zip_safe=False
)
