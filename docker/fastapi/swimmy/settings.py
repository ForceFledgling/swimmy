import os

from pydantic import BaseSettings


DB = {
    'HOST': os.environ.get("POSTGRES_HOST"),
    'DB': os.environ.get("POSTGRES_DB"),
    'USER': os.environ.get("POSTGRES_USER"),
    'PASSWORD': os.environ.get("POSTGRES_PASSWORD"),
}


class Settings(BaseSettings):
    '''Параметры конфигураций, которыми мы хотим управлять из вне'''

    server_host: str = '0.0.0.0'
    server_port: int = 8000
    database_url: str = f'postgresql://{DB["USER"]}:{DB["PASSWORD"]}@{DB["HOST"]}/{DB["DB"]}'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # в секундах


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
