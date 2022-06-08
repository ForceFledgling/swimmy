from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import Token, User, UserCreate
from ..models.roles import RoleName
from ..services.auth import AuthService, get_current_user, is_instructor_or_higher


router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/sign-up', response_model=Token)
def sign_up(
    user_data: UserCreate = Depends(),
    service: AuthService = Depends(),
):
    return service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token, name='sign-in')
def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(),
):
    return service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.get('/', response_model=List[User])
def get_users(
    role_name: Optional[RoleName] = None,
    service: AuthService = Depends(),
    user: User = Depends(is_instructor_or_higher),
):
    '''Required role to use: instructor or higher'''
    return service.get_list(role_name)


@router.get("/me", response_model=User)
def get_current_user(current_user: User = Depends(get_current_user)):
    return current_user
