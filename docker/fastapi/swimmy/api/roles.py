from fastapi import APIRouter, Depends

from ..models.auth import User
from ..models.roles import RoleName
from ..services.auth import AuthService, get_current_user, is_administrator
from ..services.roles import RoleService


router = APIRouter(
    prefix='/roles',
    tags=['roles'],
)


@router.get('/get', response_model=str)
def get_role(
    user_id: int,
    service: RoleService = Depends(),
    user: User = Depends(get_current_user),
    user_data: AuthService = Depends(),
):
    return service.get_role(user_id, user_data)


@router.put('/set', response_model=User)
def set_role(
    user_id: int,
    role_name: RoleName,
    user: User = Depends(is_administrator),
    user_data: AuthService = Depends(),
    service: RoleService = Depends(),
):
    '''Required role to use: administrator'''
    return service.set_role(user_id, user_data, role_name)
