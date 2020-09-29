import os


def sort_directories(directories):
    root = {}
    list_1 = []
    for x in directories:
        list_1.append(os.path.split(x))
    for x in range(1, max([len(x) for x in list_1])+1):
        for item in list_1:
            if len(item) == x:
                root[item[-1]] = {}
    return root


def get(path, root):
    path = os.path.split(path)
    temporary = root
    for x in path:
        temporary = temporary[x]
    return temporary
