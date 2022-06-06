from typing import List

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import User
from ..models.groups import Group, GroupBase, GroupCreate, GroupDetailed, GroupUpdate
from .. services.auth import AuthService
from ..services.rooms import RoomService


class GroupService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_group_by_name(self, group_name: str) -> tables.Group:
        '''Получаем группу по имени группы'''
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
        '''Получаем конкретную группу по id группы'''
        group = (
            self.session
            .query(tables.Group)
            .filter_by(id=group_id)
            .first()
        )
        if not group:
            raise HTTPException(status_code=406, detail='Group with this id does not exist') from None
        return group

    def _get_group_instructor(self, group_id):
        '''Проверяем что инструктор входит в группу'''
        entry = (
            self.session
            .query(tables.GroupInstructor)
            .filter_by(
                group_id=group_id,
            )
            .first()
        )
        if entry:
            user = AuthService._get(self, entry.instructor_id)
            return user.username

    def _get_groups_by_member_id(self, user_id: int) -> tables.GroupMember:
        '''Для инструкторов и клиентов'''
        groups = (
            self.session
            .query(tables.GroupMember)
            .filter_by(member_id=user_id)
            .all()
        )
        if not groups:
            raise HTTPException(status_code=406, detail='This user is not a member of groups') from None
        return groups

    def get_list(self) -> List[tables.Group]:
        '''Получаем все записи из таблицы с группами'''
        groups = (
            self.session
            .query(tables.Group)
            .all()
        )

        groups_detailed = []
        for group in groups:
            group = Group.from_orm(group)
            instructor_name = self._get_group_instructor(group.id)
            group = GroupDetailed(**group.dict(), instructor=instructor_name)
            groups_detailed.append(group)
        return groups_detailed

    # def get_list(self) -> List[tables.Group]:
    #     '''Получаем все записи из таблицы с группами'''
    #     groups = (
    #         self.session
    #         .query(tables.Group)
    #         .all()
    #     )
    #     return groups

    def get_list_instructors(self) -> List[tables.GroupInstructor]:
        '''Получаем все записи из таблицы с инструкторами всех групп'''
        groups = (
            self.session
            .query(tables.GroupInstructor)
            .all()
        )
        return groups

    def get_list_members(self) -> List[tables.GroupMember]:
        '''Получаем все записи из таблицы с участниками всех групп'''
        groups = (
            self.session
            .query(tables.GroupMember)
            .all()
        )
        return groups

    def get(self, group_id: int) -> tables.Group:
        '''Получаем группу по id группы'''
        return self._get(group_id)

    def get_my_groups(self, user: User = Depends()) -> tables.GroupMember:
        groups = GroupService._get_groups_by_member_id(self, user.id)
        return groups

    def create(self, group_data: GroupCreate, room_data: RoomService) -> tables.Group:
        '''Создаем группу'''
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
        '''Обновляем информацию о группе'''
        group = self._get(group_id)
        for field, value in group_data:
            setattr(group, field, value)
        self.session.commit()
        return group

    def delete(self, group_id) -> None:
        '''Удаляем группу'''
        group = self._get(group_id)
        self.session.delete(group)
        self.session.commit()

    def _check_group_member(self, group_id, member_id):
        '''Проверяем что пользователь входит в группу'''
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

    def _check_group_instructor(self, group_id, instructor_id):
        '''Проверяем что инструктор входит в группу'''
        entry = (
            self.session
            .query(tables.GroupInstructor)
            .filter_by(
                group_id=group_id,
                instructor_id=instructor_id,
            )
            .first()
        )
        if entry:
            return entry

    def get_busy_places_count(self, group_id) -> List:
        '''Получаем списком количество занятых мест в группе мужских/женских'''
        male_busy_count = (
            self.session
            .query(tables.GroupMember)
            .filter_by(
                group_id=group_id,
                member_sex='male',
            )
            .count()
        )
        female_busy_count = (
            self.session
            .query(tables.GroupMember)
            .filter_by(
                group_id=group_id,
                member_sex='female',
            )
            .count()
        )
        return [male_busy_count, female_busy_count]

    def join(self, group_id: int, user: User) -> tables.GroupMember:
        '''Клиент присоеденяется к плавательной группе'''
        if user.role_name != 'client':
            raise HTTPException(status_code=406, detail='The user is not a client') from None

        busy_places_count = self.get_busy_places_count(group_id)
        busy_places_male = busy_places_count[0]
        busy_places_female = busy_places_count[1]

        if user.sex.name == 'male':
            group_capacity_male = GroupService.get(self, group_id).max_mans
            if busy_places_male == group_capacity_male:
                raise HTTPException(status_code=406, detail='All places for male in this group are filled') from None
        if user.sex.name == 'female':
            group_capacity_female = GroupService.get(self, group_id).max_mans
            if busy_places_female == group_capacity_female:
                raise HTTPException(status_code=406, detail='All places for female in this group are filled') from None

        group_member = self._check_group_member(group_id, user.id)
        if group_member:
            raise HTTPException(status_code=406, detail='The user is already a member of this group') from None
        group_member = tables.GroupMember(
            group_id=group_id,
            member_id=user.id,
            member_sex=user.sex,
        )
        self.session.add(group_member)
        self.session.commit()
        return group_member

    def leave(self, group_id: int, user: User) -> str:
        '''Клиент покидает плавательную группу'''
        group_member = self._check_group_member(group_id, user.id)
        if group_member is None:
            raise HTTPException(status_code=406, detail='The user is not a member of a group') from None
        self.session.delete(group_member)
        self.session.commit()
        return 'OK'

    def add_member(self, group_id: int, user_id: int) -> tables.GroupMember:
        '''Инструктор или админимтсратор могут добавить пользователя в плавательную группу'''
        user = AuthService._get(self, user_id)
        user = User.from_orm(user)
        group_member = GroupService.join(self, group_id, user)
        return group_member

    def delete_member(self, group_id: int, user_id: int) -> tables.GroupMember:
        '''Инструктор или админимтсратор могут удалить пользователя из плавательной группы'''
        group_member = self._check_group_member(group_id, user_id)
        if group_member is None:
            raise HTTPException(status_code=406, detail='The user is not a member of a group') from None
        self.session.delete(group_member)
        self.session.commit()
        return 'OK'

    def add_instructor(self, group_id: int, instructor_id: int) -> tables.GroupInstructor:
        '''Админимтсратор может добавить инструктора в плавательную группу'''
        user = (self.session.query(tables.User).filter_by(id=instructor_id).first())
        if not user:
            raise HTTPException(status_code=406, detail='User with this id does not exist') from None
        if user.role_name != 'instructor':
            raise HTTPException(status_code=406, detail='The user is not an instructor') from None

        group_instructor = self._check_group_instructor(group_id, instructor_id)
        if group_instructor:
            raise HTTPException(status_code=406, detail='The instructor is already a member of this group') from None
        else:
            group_instructor = tables.GroupInstructor(
                group_id=group_id,
                instructor_id=instructor_id,
            )

        self.session.add(group_instructor)
        self.session.commit()
        return group_instructor

    def delete_instructor(self, group_id: int, instructor_id: int) -> tables.GroupInstructor:
        '''Администратор может удалить инструктора из плавательной группы'''
        group_instructor = self._check_group_instructor(group_id, instructor_id)
        if group_instructor is None:
            raise HTTPException(status_code=406, detail='The instructor is not a member of a group') from None

        self.session.delete(group_instructor)
        self.session.commit()
        return 'OK'
