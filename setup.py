import setuptools

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="pydenver",
    packages=["denver"],
    version="1.0.0",
    author="xcodz",
    description="Denver API for python full-stack development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8"
)
