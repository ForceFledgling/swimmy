from fastapi import Depends

from .auth import AuthService
from .. import tables
from ..database import Session, get_session
from ..models.auth import User
from ..models.roles import RoleBase, RoleName


class RoleService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_role(self, user_id: int, user_data: AuthService) -> RoleBase:
        user = user_data.get(user_id)
        return user.role_name

    def set_role(self, user_id: int, user_data: User, role_name: RoleName) -> tables.User:
        user = user_data.get(user_id)
        role_feild = 'role_name'
        setattr(user, role_feild, role_name)
        self.session.commit()
        return user
