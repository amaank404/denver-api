import denver
import shutil
import pickle


def install_app(root: str, assets_root: str):
    with open(f"{root}/requirements.pickle", "r+b") as file:
        requirements = pickle.load(file)
    print(f"Installing Requirements: {requirements}")
    for x in requirements:
        if denver.install_pip_package(requirements) != 0:
            print(f"Error: Unable to install: {x}")
            return False

    shutil.copytree("main", f"{root}/main")
    shutil.copytree("lib", f"{root}/lib")
    shutil.copyfile("app.json", f"{root}/app.json")
    shutil.copyfile("icon.cpg", f"{root}/icon.cpg")
    shutil.copytree("assets", assets_root)
