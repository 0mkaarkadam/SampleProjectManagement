import json
import os

BASE_DIR = "db"


def get_file_path(filename):
    os.makedirs(BASE_DIR, exist_ok=True)
    return os.path.join(BASE_DIR, filename)


def read_data(filename):
    path = get_file_path(filename)

    if not os.path.exists(path):
        return []

    with open(path, "r") as f:
        return json.load(f)


def write_data(filename, data):
    path = get_file_path(filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)