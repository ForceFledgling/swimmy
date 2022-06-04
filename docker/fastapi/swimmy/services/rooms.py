from typing import List

from fastapi import Depends, HTTPException

from .. import tables
from ..database import Session, get_session
from ..models.rooms import RoomCreate, RoomUpdate


class RoomService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_capacity_rooms(self):
        rooms = (
            self.session
            .query(tables.Room)
            .all()
        )
        capacity_male = capacity_female = 0
        for room in rooms:
            if room.sex == 'male':
                capacity_male += room.capacity
            elif room.sex == 'female':
                capacity_female += room.capacity
        return [capacity_male, capacity_female, capacity_male + capacity_female]

    def _get(self, room_id: int) -> tables.Room:
        room = (
            self.session
            .query(tables.Room)
            .filter_by(id=room_id)
            .first()
        )
        if not room:
            raise HTTPException(status_code=406, detail='Room with this id does not exist') from None

        return room

    def get(self, room_id: int) -> tables.Room:
        return self._get(room_id)

    def get_list(self) -> List[tables.Room]:
        rooms = (
            self.session
            .query(tables.Room)
            .all()
        )
        return rooms

    def create(self, room_data: RoomCreate) -> tables.Room:
        room = tables.Room(**room_data.dict())
        self.session.add(room)
        self.session.commit()
        return room

    def update(self, room_id: int, room_data: RoomUpdate) -> tables.Room:
        room = self._get(room_id)
        for field, value in room_data:
            setattr(room, field, value)
        self.session.commit()
        return room

    def delete(self, room_id) -> None:
        room = self._get(room_id)
        self.session.delete(room)
        self.session.commit()
