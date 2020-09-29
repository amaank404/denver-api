import yaml


def read(path):
    with open(path) as file:
        data = yaml.safe_load(file)
    return data


def write(path, data):
    with open(path, "w") as file:
        yaml.safe_dump(data, file)
