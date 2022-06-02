from typing import List

from fastapi import APIRouter, Depends, Response, status

from ..models.groups import Group, GroupCreate, GroupUpdate, GroupMember
from ..services.auth import User, get_current_user, is_administrator, is_instructor_or_higher
from ..services.groups import GroupService

router = APIRouter(
    prefix='/groups',
    tags=['groups'],
)


@router.get('/', response_model=List[Group])
def get_groups(
    service: GroupService = Depends(),
    user: User = Depends(get_current_user),
):
    '''Required role to use: instructor or higher
    ПОКАЗЫВАТЬ КОЛ-ВО ЗАНЯТЫХ и СВОБОДНЫХ МЕСТ
    '''
    return service.get_list()


@router.get('/{group_id}', response_model=Group)
def get_group(
    group_id: int,
    user: User = Depends(is_instructor_or_higher),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**
    ДОБАВИТЬ СЮДА ОТОБРАЖЕНИЕ МЕМБЕРОВ ИЛИ КУДА
    '''
    return service.get(group_id)


@router.post('/', response_model=Group)
def create_group(
    group_data: GroupCreate = Depends(),
    user: User = Depends(is_administrator),
    service: GroupService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.create(group_data)


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


@router.put('/join/{group_id}', response_model=GroupMember)
def join_the_group(
    group_id: int,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    '''The client can choose and sign up for the desired group'''
    return service.join(group_id, user)


@router.put('/leave/{group_id}', response_model=str)
def leave_the_group(
    group_id: int,
    user: User = Depends(get_current_user),
    service: GroupService = Depends(),
):
    '''The client can leave the group'''
    return service.leave(group_id)
