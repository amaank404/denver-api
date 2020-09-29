import pickle


def read(path):
    with open(path) as file:
        data = pickle.load(file)
    return data


def write(path, data):
    with open(path) as file:
        pickle.dump(data, file)
