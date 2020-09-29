from . import get_format_reader
import os


class stream:
    def __init__(self, parsed_url):
        self.io_module = get_format_reader(parsed_url[2])
        self.url = parsed_url

    def list_directory(self, root):
        pass

    def get_file(self, path):
        pass

    def write_file(self, path, reading_stream):
        pass

    def make_directory(self, path):
        pass

    def remove_directory(self, path):
        pass

    def remove_file(self, path):
        pass

    def apply_patch(self, patch_file):
        pass
