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
