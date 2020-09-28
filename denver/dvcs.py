"""
Denver Version Control System
=============================

Status: In Development (Contributions appreciated)
In order for your work to be considered:
    *No Typos
    *Standard PEP8 Compatible
    *Must Support Python 3.8
    *Doctest (Optional)
"""

__author__ = "xcodz-dot"  # I will add your name here if you contribute
__version__ = "1.0.0"  # Semantic versioning

# Basic Idea
#  GitHub like System (Almost The same, testing will be held on lan, all test configuration
#                      for the following are stored in the project. Configurations are made
#                      using Pycharm IDE, so you might need to use it for accessing configurations.)
#  Must be using `denver.bdtp` for big data transferring (Data which is big enough 10000 bytes+)
#  Repository can be forked or cloned

# Below is the Base classes and function without any code, (You can add or remove them, also add code)


class DenverRepository:
    def __init__(self, name: str, origin: str):
        self.name = name
        self.origin = origin


# TODO ArgParse CLI
def main():
    pass


if __name__ == '__main__':
    main()
