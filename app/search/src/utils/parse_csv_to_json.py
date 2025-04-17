import csv

from pymongo import MongoClient


def parse_csv_to_mongodb(
    csv_file_path, mongo_connection_uri, database_name, collection_name
):
    client = MongoClient(mongo_connection_uri)
    db = client[database_name]
    collection = db[collection_name]

    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            course_data = {
                "description": row.get("description", "").strip(),
                "number": row.get("number", "").strip(),
                "title": row.get("title", "").strip(),
                "units": row.get("units", "").strip(),
                "requiredCourses": [
                    value
                    for i in range(20)
                    if (value := row.get(f"requiredCourses[{i}]", "").strip())
                ]
                or [],
                "courseObjectives": [
                    value.lstrip("\ufe63").strip()
                    for i in range(16)
                    if (value := row.get(f"courseObjectives[{i}]", "").strip())
                ]
                or [],
                "studentLearningOutcomes": [
                    value
                    for i in range(24)
                    if (value := row.get(f"studentLearningOutcomes[{i}]", "").strip())
                ]
                or [],
            }
            course_data = {
                key: (
                    value
                    if value
                    else []
                    if key
                    in {
                        "requiredCourses",
                        "courseObjectives",
                        "studentLearningOutcomes",
                    }
                    else ""
                )
                for key, value in course_data.items()
            }
            collection.insert_one(course_data)

    print("Data successfully inserted into MongoDB")


csv_file_path = "bt_courses.csv"
mongo_connection_uri = (
    "mongodb+srv://rathodvikram44:rathodvikram44@allcourses.l4lqk7e.mongodb.net/"
)
database_name = "allcourses"
collection_name = "allcourses"

parse_csv_to_mongodb(
    csv_file_path, mongo_connection_uri, database_name, collection_name
)
