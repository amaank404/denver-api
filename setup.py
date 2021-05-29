import os

import setuptools

with open("README.md") as file:
    long_description = file.read()


def exclude_files(filespath: list, exts: list):
    rml = []
    for x in range(len(filespath)):
        if os.path.splitext(filespath[x])[1] in exts:
            rml.append(filespath[x])
    for x in rml:
        filespath.remove(x)


def find_package_data(package: str, package_name=None):
    if package_name is None:
        package_name = package
    files = []
    for r, d, f in os.walk(package):
        files.extend([os.path.join(r, x)[len(package) + 1 :] for x in f])
    exclude_files(files, [".py"])
    root = {}
    for x in files:
        d = x.split(os.sep)
        d.pop(-1)
        d = ".".join(d)
        root.setdefault(package_name + "." + d, [])
        root[package_name + "." + d].append(os.path.basename(x))
    return {k.strip("."): v for k, v in root.items()}


setuptools.setup(
    name="denver_api",
    packages=setuptools.find_packages()
    + setuptools.find_namespace_packages(include=["denverapi", "denverapi.*"]),
    package_data=find_package_data("denverapi", "denverapi"),
    version="3.0.0",
    author="xcodz",
    description="Denver API for python full-stack development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "setuptools>50",
        "requests",
        "playsound",
        "packaging",
        "pip>=21",
        "ansiwrap",
    ],
    extras_require={
        "gui-tools": ["pygame"],
        "all": ["pygame", "pycryptodomex"],
        "encryption": ["pycryptodomex"],
    },
    entry_points={
        "console_scripts": [
            # clinetools
            "rmrdir = denverapi.clineutils.rmrdir:main",
            "rmr = denverapi.clineutils.rmr:main",
            # tools
            "bdtpserver = denverapi.tools.bdtpserver:main",
            "graphics3d-mview = denverapi.graphics3d:main [gui-tools]",
            "cryptify = denverapi.tools.cryptify:main [encryption]",
            "denverdb = denverapi.tools.denverdb:main",
        ]
    },
    zip_safe=False,
    url="https://github.com/xcodz-dot/denver-api",
)
