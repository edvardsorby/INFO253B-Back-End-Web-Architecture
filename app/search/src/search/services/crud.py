from bson import ObjectId
from pymongo import AsyncMongoClient

from search.models import Course, CourseUpdate


async def get_course(id: str, db: AsyncMongoClient) -> Course:
    result = await db.find_one({"_id": ObjectId(id)})
    if result:
        result["_id"] = str(result["_id"])
    return result


async def add_course(course: Course, db: AsyncMongoClient) -> Course:
    new_course = await db.insert_one(course.model_dump())
    return {"_id": str(new_course.inserted_id), **course.model_dump()}


async def update_course(id: str, course: CourseUpdate, db: AsyncMongoClient) -> Course:
    updated = await db.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": course.model_dump(exclude_unset=True)},
        return_document=True,
    )
    if updated:
        updated["_id"] = str(updated["_id"])
    return updated


async def delete_course(id: str, db: AsyncMongoClient) -> str:
    deleted_course = await db.find_one_and_delete({"_id": ObjectId(id)})
    return "Course deleted" if deleted_course else "Course not found"
