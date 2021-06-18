"""
Converts multiple files into one file without compression

### How does this work?
It takes the provided files and convert them into a long uncompressed stream
that can be used by programs that want to download and install things at the
same time.

### Why to use it?
You can use it to implement a http server that can provide multiple files in
a single request instead of flooding the server with multiple requests.

### Guide
"""

import io
from typing import IO, List, Union

class MultifileStreamFile:
    def __init__(self, streams: List[Union[str, IO]]):
        pass
