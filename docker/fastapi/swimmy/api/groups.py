from typing import List

from fastapi import APIRouter, Depends, Response, status

from ..models.groups import Group, GroupCreate, GroupDetailed, GroupInstructor, GroupMember, GroupUpdate
from ..services.auth import User, get_current_user, is_administrator, is_instructor_or_higher, is_not_administrator
from ..services.groups import GroupService
from ..services.rooms import RoomService

router = APIRouter(
    prefix='/groups',
    tags=['groups'],
)


@router.get('/', response_model=List[GroupDetailed], name='get groups')
def get_groups(
    service: GroupService = Depends(),
    # user: User = Depends(get_current_user),
):
    return service.get_list()


@router.get('/{group_id}', response_model=Group)
def get_group(
    group_id: int,
    user: User = Depends(is_instructor_or_higher),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.get(group_id)


@router.post('/', response_model=Group)
def create_group(
    group_data: GroupCreate = Depends(),
    room_data: RoomService = Depends(),
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.create(group_data, room_data)


@router.put('/{group_id}', response_model=Group)
def update_group(
    group_id: int,
    group_data: GroupUpdate = Depends(),
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.update(group_id, group_data)


@router.delete('/{group_id}')
def delete_group(
    group_id: int,
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    service.delete(group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post('/member/{group_id}', response_model=GroupMember)
def join_the_group(
    group_id: int,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    '''The client can choose and sign up for the desired group'''
    return service.join(group_id, user)


@router.delete('/member/{group_id}', response_model=str)
def leave_the_group(
    group_id: int,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    '''The client can leave the group'''
    return service.leave(group_id, user)


@router.get('/members/', response_model=List[GroupMember])
def get_group_members(
    service: GroupService = Depends(),
    user: User = Depends(is_instructor_or_higher),
):
    '''**Required role to use: instructor or high**'''
    return service.get_list_members()


@router.get('/members/me', response_model=List[GroupMember])
def get_my_groups(
    user: User = Depends(is_not_administrator),
    service: GroupService = Depends(),
):
    '''Required role to use: instructor or client'''
    return service.get_my_groups(user)


@router.post('/members/', response_model=GroupMember)
def add_member_to_group(
    group_id: int,
    user_id: int,
    user: User = Depends(is_instructor_or_higher),
    service: GroupService = Depends(),
):
    '''**Required role to use: instructor or high**'''
    return service.add_member(group_id, user_id)


@router.delete('/members/', response_model=str)
def delete_member_from_group(
    group_id: int,
    user_id: int,
    user: User = Depends(is_instructor_or_higher),
    service: GroupService = Depends(),
):
    '''**Required role to use: instructor or high**'''
    return service.delete_member(group_id, user_id)


@router.get('/instructors/', response_model=List[GroupInstructor])
def get_group_instructors(
    service: GroupService = Depends(),
    user: User = Depends(get_current_user),
):
    return service.get_list_instructors()


@router.post('/instructors/', response_model=GroupInstructor)
def add_instructor_to_group(
    group_id: int,
    user_id: int,
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.add_instructor(group_id, user_id)


@router.delete('/instructors/', response_model=str)
def delete_instructor_from_group(
    group_id: int,
    user_id: int,
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.delete_instructor(group_id, user_id)
