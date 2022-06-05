from typing import List

from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.instructors import BaseInstructorWorkingHours
from ..services.auth import AuthService


class InstructorService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user_id):
        hours = (
            self.session
            .query(tables.InstructorWorkingHours)
            .filter_by(instructor_id=user_id)
            .first()
        )
        return hours

    def get_list(self) -> List[tables.InstructorWorkingHours]:
        groups = (
            self.session
            .query(tables.InstructorWorkingHours)
            .all()
        )
        return groups

    def create(self, user_id, hours_data: Depends(BaseInstructorWorkingHours)) -> tables.InstructorWorkingHours:

        if AuthService._check_role_by_user_id(self, user_id=user_id, role_name='instructor') is None:
            raise HTTPException(status_code=406, detail='User with this id is not instructor') from None

        if self._get(user_id):
            raise HTTPException(status_code=406, detail='Hours for this instructor is aleready exist') from None

        working_hours = tables.InstructorWorkingHours(
            instructor_id=user_id,
            **hours_data.dict(),
        )

        self.session.add(working_hours)
        self.session.commit()
        return working_hours

    def delete(self, user_id):
        hours = self._get(user_id)
        if hours is None:
            raise HTTPException(status_code=406, detail='Hours for this instructor not exist') from None
        self.session.delete(hours)
        self.session.commit()
        return 'OK'
