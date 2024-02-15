import enum
import os.path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL


class LogLevel(enum.StrEnum):
    """Возможные уровни логгирования."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class PaymentType(enum.StrEnum):
    """доступные типы оплаты"""
    SBP: str = "sbp"
    SITE_BALANCE: str = "site_balance"


# разрешенные типы данных для загрузки в /api/upload
ALLOWED_UPLOAD_TYPES = ['image/jpeg', 'image/png', 'text/plain']


class ProductExt:
    """типы расширений для файлов-товаров для проверки при выдаче"""
    TXT = ".txt"


class Settings(BaseSettings):
    """
    Настройки приложения

    Изменяются и задаются в .env
    """

    # конфигурация uvicorn
    host: str = "127.0.0.1"
    port: int = 8000

    # количество воркеров uvicorn
    workers_count: int = 1

    # Обновление uvicorn
    reload: bool = False

    # Текущее окружение
    environment: str = "dev"

    log_level: LogLevel = LogLevel.DEBUG

    # типы оплаты (платежки)
    payment_types: list[str] = [PaymentType.SBP, PaymentType.SITE_BALANCE]

    # Данные от базы данных
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_base: str = "axegaoshopdb"
    db_echo: bool = False

    # конфигурация Sentry SDK
    sentry_dsn: Optional[str] = None
    sentry_sample_rate: float = 1.0

    storage_folder: str = "axegaoshop/data/storage"

    # картинки сайта
    storage_folder_images: str = storage_folder + "/uploads"

    jwt_secret_key: str = "jwt_key"
    jwt_refresh_secret_key: str = "jwt_refresh_key"

    @property
    def db_url(self) -> URL:
        """
        Создание ссылки для подключения к базе данных

        :return: database URL.
        """
        return URL.build(
            scheme="asyncpg",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_password,
            path=f"/{self.db_base}",
        )

    def __call__(self):
        """создание папок для хранилища"""
        os.makedirs(self.storage_folder, exist_ok=True)
        os.makedirs(self.storage_folder_images, exist_ok=True)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AXEGAOSHOP_",
        env_file_encoding="utf-8",
    )


settings = Settings()
settings.__call__()
