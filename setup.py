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
    version="2.5.5b0",
    author="xcodz",
    description="Denver API for python full-stack development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        "requests",
        "playsound",
        "cryptography",
        "packaging",
    ],
    extras_require={"gui-tools": ["pygame"]},
    entry_points={
        "console_scripts": [
            # clinetools
            "rmrdir = denverapi.clineutils.rmrdir:main",
            "rmr = denverapi.clineutils.rmr:main",
            # tools
            "bdtpserver = denverapi.tools.bdtpserver:main",
            "cpicview = denverapi.tools.cpicview:main",
            "cpic_editor = denverapi.tools.cpic_editor:fromcmd [gui-tools]",
        ]
    },
    zip_safe=False,
)
