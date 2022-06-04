from typing import List

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import User
from ..models.groups import GroupCreate, GroupUpdate
from ..services.rooms import RoomService


class GroupService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_group_by_name(self, group_name: str) -> tables.Group:
        group = (
            self.session
            .query(tables.Group)
            .filter_by(name=group_name)
            .first()
        )
        if not group:
            return None
        return group

    def _get(self, group_id: int) -> tables.Group:

        group = (
            self.session
            .query(tables.Group)
            .filter_by(id=group_id)
            .first()
        )
        if not group:
            raise HTTPException(status_code=406, detail='Group with this id does not exist') from None

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

    def create(self, group_data: GroupCreate, room_data: RoomService) -> tables.Group:

        if self._get_group_by_name(group_data.name):
            raise HTTPException(status_code=406, detail='Group with this name is already exist') from None

        room_capacity_male, room_capacity_female, room_capacity_all = room_data._get_capacity_rooms()

        group = tables.Group(
            **group_data.dict(),
            places=room_capacity_all,
            free_places=10,
            max_mans=room_capacity_male,
            max_womans=room_capacity_female,
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
                member_id=member_id,
            )
            .first()
        )
        if entry:
            return entry

    def join(self, group_id: int, user: User) -> tables.GroupMember:

        group_member = self._check_group_member(group_id, user.id)
        if group_member:
            raise HTTPException(status_code=406, detail='The user is already a member of this group') from None

        group_member = tables.GroupMember(
            group_id=group_id,
            member_id=user.id,
        )
        self.session.add(group_member)
        self.session.commit()
        return group_member

    def leave(self, group_id: int, user: User) -> str:

        group_member = self._check_group_member(group_id, user.id)
        if group_member is None:
            raise HTTPException(status_code=406, detail='The user is not a member of a group') from None

        self.session.delete(group_member)
        self.session.commit()
        return 'OK'

    def add_member(self, group_id: int, user_id: int) -> tables.GroupMember:

        group_member = self._check_group_member(group_id, user_id)
        if group_member:
            raise HTTPException(status_code=406, detail='The user is already a member of this group') from None
        else:
            group_member = tables.GroupMember(
                group_id=group_id,
                member_id=user_id,
            )

        self.session.add(group_member)
        self.session.commit()
        return group_member

    def delete_member(self, group_id: int, user_id: int) -> tables.GroupMember:

        group_member = self._check_group_member(group_id, user_id)
        if group_member is None:
            raise HTTPException(status_code=406, detail='The user is not a member of a group') from None

        self.session.delete(group_member)
        self.session.commit()
        return 'OK'
