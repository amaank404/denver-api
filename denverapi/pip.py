"""
Useful utilities for manipulating pypi requests or pip requests.
"""

import requests
import urllib.parse as urlparse
import json


class FailedDownloadStatusCode(Exception):
    pass


class Index:
    def __init__(self, root: str, project: str, json: str):
        self.root = root
        self.project = urlparse.urljoin(root, project)
        self.project = urlparse.urljoin(root, json)

    def get_root(self) -> str:
        return self.root

    def get_project(self, name: str) -> str:
        return self.project.format(project=name)

    def get_json(self, name: str) -> str:
        return self.project.format(project=name)


pypi = Index("https://pypi.org/", "/project/{project}", "/pypi/{project}/json")


def download_data(url: str):
    result = requests.get(url)
    if not result.ok:
        raise FailedDownloadStatusCode(result.status_code)
    return result.content


def download_data_text(url: str):
    download_data(url).decode("utf-8")
