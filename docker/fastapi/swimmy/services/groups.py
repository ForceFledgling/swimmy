from typing import List

from fastapi import Depends, HTTPException, status

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import User
from ..models.groups import GroupCreate, GroupMember, GroupMemberBase, GroupUpdate


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
        group = tables.Group(
            **group_data.dict(),
            places=10,
            free_places=10,
            max_mans=6,
            max_womans=4,
            members_id=(1, 2, 3, 4),
        )
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

    def _check_group_member(self, group_id, member_id):
        entry = (
            self.session
            .query(tables.GroupMember)
            .filter_by(
                group_id=group_id,
                member_id=member_id
            )
            .first()
        )
        if not entry:
            return False
        return True

    def join(self, group_id: int, user: User) -> tables.GroupMember:
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='The user is already a member of this group',
            headers={
                'WWW-Authenticate': 'Bearer',
            },
        )

        check_user = self._check_group_member(group_id, user.id)
        if check_user is True:
            raise exception

        group_member = tables.GroupMember(
            group_id=group_id,
            member_id=user.id,
        )
        self.session.add(group_member)
        self.session.commit()
        return group_member

    def leave(self, group_id: int) -> tables.Group:
        group = self._get(group_id)
        # setattr(group, field, value)
        # self.session.commit()
        # print('1111111111group.members_id', type(set(group.members_id)), set(group.members_id))
        return group
