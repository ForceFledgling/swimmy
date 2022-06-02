from typing import List

from fastapi import APIRouter, Depends, Response, status

from ..models.auth import User
from ..models.rooms import Room, RoomCreate, RoomUpdate
from ..services.auth import is_administrator, is_instructor_or_higher
from ..services.rooms import RoomService


router = APIRouter(
    prefix='/rooms',
    tags=['rooms'],
)


@router.get('/', response_model=List[Room])
def get_rooms(
    service: RoomService = Depends(),
    user: User = Depends(is_instructor_or_higher),
):
    '''Required role to use: instructor or higher'''
    return service.get_list()


@router.post('/', response_model=Room)
def create_room(
    room_data: RoomCreate = Depends(),
    service: RoomService = Depends(),
    user: User = Depends(is_administrator),
):
    '''**Required role to use: administrator**'''
    return service.create(room_data)


@router.get('/{room_id}', response_model=Room)
def get_room(
    room_id: int,
    service: RoomService = Depends(),
    user: User = Depends(is_instructor_or_higher),
):
    '''Required role to use: instructor or higher'''
    return service.get(room_id)


@router.put('/{room_id}', response_model=Room)
def update_room(
    room_id: int,
    room_data: RoomUpdate = Depends(),
    user: User = Depends(is_administrator),
    service: RoomService = Depends(),
):
    '''**Required role to use: administrator**'''
    return service.update(room_id, room_data)


@router.delete('/{room_id}')
def delete_room(
    room_id: int,
    user: User = Depends(is_administrator),
    service: RoomService = Depends(),
):
    '''**Required role to use: administrator**'''
    service.delete(room_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
