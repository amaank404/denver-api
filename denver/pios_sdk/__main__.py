import os


def tool(path):
    p = os.path.basename(path)
    p = os.path.splitext(p)[0]
    return p


if __name__ == '__main__':
    directory = os.path.dirname(__file__)
    print("Available SDK Tools:")
    for x in os.listdir(directory):
        if not x.startswith("_") and x.endswith(".py"):
            print("\t"+tool(x))
