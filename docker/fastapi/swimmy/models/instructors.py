from datetime import time

from pydantic import BaseModel


class BaseInstructorWorkingHours(BaseModel):
    min_hours: int
    max_hours: int
    preferred_start: time
    preferred_end: time


class InstructorWorkingHours(BaseInstructorWorkingHours):
    id: int
    instructor_id: int

    class Config:
        orm_mode = True
