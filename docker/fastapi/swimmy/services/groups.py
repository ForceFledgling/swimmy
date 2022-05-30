from typing import List

from fastapi import Depends

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session


class GroupService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_list(self) -> List[tables.Group]:
        groups = (
            self.session
            .query(tables.Group)
            .all()
        )
        return groups
