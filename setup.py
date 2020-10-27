import setuptools
from denverapi import pysetup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="denverapi",
    packages=setuptools.find_packages(),
    package_data=pysetup.find_package_data("denverapi", "denverapi"),
    version="2.2.1",
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
    ],
    entry_points={
        "console_scripts": [
            "denverapi-cpic-edit = denverapi.tools.cpic_editor",
            "denverapi-bdtpserver = denverapi.tools.bdtpserver",
        ]
    },
    zip_safe=False
)
