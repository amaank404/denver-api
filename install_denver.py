#  Copyright (c) 2020 Xcodz.
#  All Rights Reserved.
import os

import requests
import configparser
import argparse
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Denver API Installer",
                                     description="This is software installer for Denver API, to use it you require a "
                                                 "active Internet Access")
    parser.add_argument("-c", "--conf", metavar="ConfigurationFile", action="store", required=False,
                        default="./installer_info/dn.ini")
    parser.add_argument("-d", "--dir", action="store", required=False, default=".", metavar="DirectoryToInstall")
    args = parser.parse_args()

    # Configuration Loading
    configuration = configparser.ConfigParser(interpolation=None)
    configuration.read_string(open(args.conf).read(), "DenverConfiguration")
    configuration = configuration["Denver"]

    # User Interface
    print("Powered by", configuration["DownloadSite"])
    print("\nPreparing to get File")
    url = str(configuration["DownloadLink"])
    print(f"Downloading \"{url}\"")
    page = requests.get(url)
    print("Writing \"Denver.zip\"")
    with open("Denver.zip", "w+b") as file:
        file.write(page.content)
    print("Unpacking \"Denver.zip\"")
    shutil.unpack_archive("Denver.zip", args.dir)
    print("Deleting \"Denver.zip\"")
    os.remove("Denver.zip")
    print("Target Complete")
