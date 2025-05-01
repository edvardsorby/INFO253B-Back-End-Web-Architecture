from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

# class Course(BaseModel):
#     number: str
#     title: str
#     description: str
#     units: str
#     required_courses: list[str]
#     course_objectives: list[str]
#     student_learning_outcomes: list[str]
#     embedding: list[float] | None = None


class Course(BaseModel):
    url: str
    term_name: str | None = None
    department: str | None = None
    course_number: str | None = None
    section_id: str | None = None
    course_title: str | None = None
    special_title: str | None = None
    instructor: str | None = None
    catalog_description: str | None = None
    class_description: str | None = None
    location: str | None = None
    embedding: list[float] | None = None


class SearchOut(Course):
    score: float


class MessagesIn(BaseModel):
    query: str
    conv_id: UUID | None


class MessagesOut(BaseModel):
    response: str
    conv_id: UUID

class CourseUpdate(BaseModel):
    url: Optional[str] = None
    term_name: Optional[str] | None = None
    department: Optional[str] | None = None
    course_number: Optional[str] | None = None
    section_id: Optional[str] | None = None
    course_title: Optional[str] | None = None
    special_title: Optional[str] | None = None
    instructor: Optional[str] | None = None
    catalog_description: Optional[str] | None = None
    class_description: Optional[str] | None = None
    location: Optional[str] | None = None

    model_config = ConfigDict(extra="forbid")
