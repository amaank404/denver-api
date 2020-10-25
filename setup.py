import setuptools
from denver import pysetup

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="pydenver",
    packages=setuptools.find_packages(include=["denver.*"])+setuptools.find_namespace_packages(include=["denver.*"]),
    package_data=pysetup.find_package_data("denver", "denver"),
    version="2.2.0",
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
        "getmac",
        "cryptography"
    ],
    extras_require={
        "PiOS": ["pydenver_pios_sdk"]
    },
    entry_points={
        "console_scripts": [
            "pios-sdk-ppk = denver.pios_sdk.ppk [PiOS]",
            "pios-sdk-app = denver.pios_sdk.app [PiOS]",
            "pios-sdk-gensha256 = denver.pios_sdk.generate_sha256 [PiOS]",
            "denver-cpic-edit = denver.tools.cpic_editor",
            "denver-bdtpserver = denver.tools.bdtpserver",
            "denver-pybuild = denver.tools.pybuild [PiOS]"
        ]
    },
    zip_safe=False
)
