from typing import List

from fastapi import APIRouter, Depends, Response, status

from ..models.groups import Group, GroupCreate, GroupUpdate
from ..services.groups import GroupService

router = APIRouter(
    prefix='/groups',
)


@router.get('/', response_model=List[Group])
def get_groups(service: GroupService = Depends()):
    return service.get_list()


@router.post('/', response_model=Group)
def create_group(
    group_data: GroupCreate,
    service: GroupService = Depends(),
):
    return service.create(group_data)


@router.get('/{group_id}', response_model=Group)
def get_group(
    group_id: int,
    service: GroupService = Depends(),
):
    return service.get(group_id)


@router.put('/{group_id}', response_model=Group)
def update_group(
    group_id: int,
    group_data: GroupUpdate,
    service: GroupService = Depends(),
):
    return service.update(
        group_id,
        group_data,
    )


@router.delete('/{group_id}')
def delete_group(
    group_id: int,
    service: GroupService = Depends(),
):
    service.delete(group_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
