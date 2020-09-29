import json


def read(path):
    with open(path) as file:
        data = json.load(file)
    return data


def write(path, data):
    with open(path, 'w') as file:
        json.dump(data, file)
