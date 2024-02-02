import os

from avatar_generator import Avatar

from data.config import Storage
from utils.helpers import random_string


def create_user_photo(username: str) -> str:
    """генерация аватарки пользователя

    # https://ui-avatars.com/
    """
    avatar = Avatar().generate(200, string=username, filetype="PNG")

    file_uid = f"{random_string()}.png"
    file_path = os.path.join(Storage.uploads, file_uid)

    with open(file_path, "wb") as f:
        f.write(avatar)

    return file_uid



