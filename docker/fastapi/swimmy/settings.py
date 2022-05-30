import os

from pydantic import BaseSettings


DB = {
    'POSTGRES_HOST': os.environ.get("POSTGRES_HOST"),
    'POSTGRES_DB': os.environ.get("POSTGRES_DB"),
    'POSTGRES_USER': os.environ.get("POSTGRES_USER"),
    'POSTGRES_PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
}


class Settings(BaseSettings):
    '''Параметры конфигураций, которыми мы хотим управлять из вне'''

    server_host: str = '0.0.0.0'
    server_port: int = 8000
    database_url: str = f'postgresql://{DB["POSTGRES_USER"]}:{DB["POSTGRES_PASSWORD"]}@{DB["POSTGRES_HOST"]}/{DB["POSTGRES_DB"]}'


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
