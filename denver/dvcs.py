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
from typing import List, Tuple, Union

DEFAULT_PORTS = {
    "dvsc": 6080,
    "fserv": 6081,
    "http": 80
}


class DenverRepository:
    def __init__(self, name: str, original: str):
        self.name = name
        self.origin = original


def update():
    pass


def parse_url(url: str) -> List[str, Union[Tuple[str, int], None], str]:
    """
    Parse a URL in format:
        {protocol}://{server_ip}:{port=protocol_default}/{path_to_file}/
    Example:
        dvsc://127.0.0.1:6744/MyRepos/repo1/denver_vsc.repo
        fserv://127.0.0.1:1245/MyRepos/repo2/denver_vsc.repo
        http://127.0.0.1:1249/MyRepos/repo3/denver_vsc.repo
        file://MyRepos/repo4/denver_vsc.repo
    Default Ports:
        dvsc = 6080
        fserv = 6081
        http = 80
        file = None
    Return Value:
        dvsc, fserv, http = [protocol, (ip, port), sub_address]
        file = ["file", None, sub_address]
    """
    url_protocol, url = url.split("://", 1)
    url_address, url_sub_address = url.split("/", 1)
    if ':' in url_address:
        url_address = tuple(url_address.split(":"))
    else:
        url_address = (url_address, DEFAULT_PORTS[url_protocol])

    if url_protocol is not "file":
        return [url_protocol, url_address, url_sub_address]
    else:
        return ["file", None, f"{url_address}/{url_sub_address}"]


# TODO ArgParse CLI
def main():
    pass


if __name__ == '__main__':
    main()
