"""
Utilities to genrate a library out of python source
"""

import runpy
from pprint import pprint

pprint(dir(runpy))

pprint(runpy._run_code("", {}))
