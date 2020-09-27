#  Copyright (c) 2020 Xcodz.
#  All Rights Reserved.

import os
import platform
import time

asctime = time.asctime()

with open('version_info.py', "w") as f:
    f.write(f"""
build_time = "{asctime}"
build_version = "1.0.0"
build_platform = "{platform.platform()}"
""")

if __name__ == '__main__':
    os.system(f'pyinstaller "sockets.py" --onefile -i favicon.ico')
