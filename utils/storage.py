import os

from data.config import Storage


def create_storage():
    if not os.path.exists(Storage.path):
        os.mkdir(Storage.path)

    if not os.path.exists(Storage.uploads):
        os.mkdir(Storage.uploads)