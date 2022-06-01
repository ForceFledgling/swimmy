from typing import List

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.groups import GroupCreate, GroupUpdate


class GroupService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, group_id: int) -> tables.Group:
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Group with this id does not exist',
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )

        group = (
            self.session
            .query(tables.Group)
            .filter_by(id=group_id)
            .first()
        )
        if not group:
            raise exception

        return group

    def get_list(self) -> List[tables.Group]:
        groups = (
            self.session
            .query(tables.Group)
            .all()
        )
        return groups

    def get(self, group_id: int) -> tables.Group:
        return self._get(group_id)

    def create(self, group_data: GroupCreate) -> tables.Group:
        group = tables.Group(**group_data.dict())
        self.session.add(group)
        self.session.commit()
        return group

    def update(self, group_id: int, group_data: GroupUpdate) -> tables.Group:
        group = self._get(group_id)
        for field, value in group_data:
            setattr(group, field, value)
        self.session.commit()
        return group

    def delete(self, group_id) -> None:
        group = self._get(group_id)
        self.session.delete(group)
        self.session.commit()
