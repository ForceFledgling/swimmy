from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, HTTPException
from fastapi.exceptions import ValidationError
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from passlib.hash import bcrypt

from .. import tables
from ..database import Session, get_session
from ..models.auth import Token, User, UserCreate
from ..models.roles import RoleName
from ..settings import settings


oath2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign-in')  # обявляем схему с формой авторизации


def get_current_user(token: str = Depends(oath2_scheme)) -> User:
    '''Получаем текущего пользователя'''
    return AuthService.validate_token(token)


def is_administrator(current_user: User = Depends(get_current_user)):
    '''Проверка, что пользователь является администратором'''
    if current_user.role_name != RoleName.administrator.name:
        raise HTTPException(status_code=400, detail="User is not administrator") from None
    return current_user


def is_instructor_or_higher(current_user: User = Depends(get_current_user)):
    if current_user.role_name not in [RoleName.instructor.name, RoleName.administrator.name]:
        raise HTTPException(status_code=400, detail="User is not instructor or high") from None
    return current_user


def is_instructor(current_user: User = Depends(get_current_user)):
    if current_user.role_name != RoleName.instructor.name:
        raise HTTPException(status_code=400, detail="User is not instructor")
    return current_user


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:

        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise HTTPException(status_code=406, detail='Could not validate credentials') from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise HTTPException(status_code=406, detail='Could not validate credentials') from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)  # преобразуем из модели orm в модел pydantic

        now = datetime.utcnow()

        payload = {
            'iat': now,  # время создания токена
            'nbf': now,  # время до которой токен нельзя использовать (в формате UTC!)
            'exp': now + timedelta(seconds=settings.jwt_expiration),  # время истечения токена
            'sub': str(user_data.id),  # обозначает пользователя которому выдан токен
            'user': user_data.dict(),  # модель пользователя в виде словаря
        }

        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:  # при регистрации так же выполняется и авторизация
        user = tables.User(
            email=user_data.email,
            username=user_data.username,
            password_hash=self.hash_password(user_data.password),
            role_name=RoleName.client.name,
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:

        user = (
            self.session
            .query(tables.User)
            .filter(tables.User.username == username)
            .first()
        )

        if not User:
            raise HTTPException(status_code=406, detail='Incorrect username or password') from None

        if not self.verify_password(password, user.password_hash):
            raise HTTPException(status_code=406, detail='Incorrect username or password') from None

        return self.create_token(user)

    def _get(self, user_id: int) -> tables.User:

        user = (
            self.session
            .query(tables.User)
            .filter_by(id=user_id)
            .first()
        )
        if not user:
            raise HTTPException(status_code=406, detail='User with this id does not exist') from None

        return user

    def get(self, user_id: int) -> tables.User:
        return self._get(user_id)

    def get_list(self, role_name: Optional[RoleName] = None) -> List[tables.User]:
        query = self.session.query(tables.User)
        if role_name:
            query = query.filter_by(role_name=role_name)
        users = query.all()
        return users
