from typing import List

from fastapi import APIRouter, Depends

from ..models.groups import Group
from ..services.groups import GroupService

router = APIRouter(
    prefix='/groups',
)


@router.get('/', response_model=List[Group])
def get_groups(group: GroupService = Depends()):
    return group.get_list()
