import os

import dotenv

dotenv.load_dotenv()


class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")

    DB_CONN_STRING: str = f"asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY = os.getenv("JWT_REFRESH_SECRET_KEY")

    DEFAULT_CATEGORIES = [
        ["Операционные системы", ""],
        ["Office", ""],
        ["Безопасность", ""],
        ["Управление бизнесом", ""],
        ["Работа с графикой и САПР", ""],
        ["Разное", ""]
    ]


class Storage:
    path: str = "data/storage"

    uploads: str = "data/storage/uploads"
