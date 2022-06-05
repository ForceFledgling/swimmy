from typing import List

from fastapi import APIRouter, Depends

from ..models.auth import User
from ..models.instructors import BaseInstructorWorkingHours, InstructorWorkingHours
from ..services.auth import is_administrator
from ..services.instructors import InstructorService


router = APIRouter(
    prefix='/instructors',
    tags=['instructors'],
)


@router.get('/', response_model=List[InstructorWorkingHours])
def get_instructors_hours(
    service: InstructorService = Depends(),
    user: User = Depends(is_administrator),
):
    return service.get_list()


@router.post('/hours', response_model=InstructorWorkingHours)
def create_working_hours(
    user_id: int,
    hours_data: BaseInstructorWorkingHours = Depends(),
    service: InstructorService = Depends(),
    user: User = Depends(is_administrator),
):
    return service.create(user_id, hours_data)


@router.delete('/hours', response_model=str)
def delete_working_hours(
    user_id: int,
    user: User = Depends(is_administrator),
    service: InstructorService = Depends(),
):
    return service.delete(user_id)
