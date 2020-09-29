from . import *
from ..dvcs_sort import *
import os


class stream:
    def __init__(self, parsed_url):
        self.url = parsed_url
        self.temp = os.path.expanduser("~/.temp")
        file_extension = os.path.splitext(parsed_url[2])[1]
        self.repository_temp = f"{self.temp}/repo{file_extension}"
        with open(parsed_url[2]) as file:
            data = file.read()
        with open(self.repository_temp, 'w') as file:
            file.write(data)
        self.io_module = get_format_reader(parsed_url[2])
        self.configuration = self.io_module.read(self.repository_temp)

    def list_directory(self, path):
        root = sort_directories(self.configuration['nav-dir'])
        return list(get(path, root).keys())

    def get_file(self, path):
        pass

    def write_file(self, path, reading_stream):
        pass

    def make_directory(self, path):
        raise IOError("")

    def remove_directory(self, path):
        pass

    def remove_file(self, path):
        pass

    def apply_patch(self, patch_file):
        pass

    def exists(self, path):
        try:
            self.list_directory(os.path.dirname(path))
            return True
        except KeyError:
            return False
