from uuid import UUID

from pydantic import BaseModel


class Course(BaseModel):
    number: str
    title: str
    description: str
    units: str
    required_courses: list[str]
    course_objectives: list[str]
    student_learning_outcomes: list[str]
    embedding: list[float] | None = None


class SearchOut(Course):
    score: float


class MessagesIn(BaseModel):
    query: str
    conv_id: UUID | None


class MessagesOut(BaseModel):
    response: str
    conv_id: UUID
