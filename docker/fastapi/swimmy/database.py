from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import settings


engine = create_engine(
    settings.database_url,
    # connect_args={'check_same_thread': False},  # на каждый запрос новая сессия (без переподключения)
)


Session = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_session() -> Session:
    '''
    Внедрение зависимостей в обработчик.
    Любой callable :
    1. Функции, классы, экземпляры классов
    2. Генераторы
    3. Асинхронные функции и генераторы
    '''
    session = Session()
    try:
        yield session  # передаем сессию в обработчик
    finally:
        session.close()
