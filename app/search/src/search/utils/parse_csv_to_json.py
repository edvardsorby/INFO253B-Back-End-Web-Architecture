import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
import voyageai
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from search.models import Course

COURSE_DOC_TEMPLATE = """\
Course Title
{title}

Course Description
{description}
"""


def add_course_embedding(
    client: voyageai.Client, course_batch: list[Course]
) -> list[float]:
    course_docs = [
        COURSE_DOC_TEMPLATE.format(title=course.title, description=course.description)
        for course in course_batch
    ]
    vectors = client.embed(
        course_docs, model="voyage-3-large", input_type="document"
    ).embeddings
    for course, vec in zip(course_batch, vectors, strict=True):
        course.embedding = vec


def add_course_embeddings(courses, concurrency=10):
    vo = voyageai.Client()

    batch_size = 128
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for i in range(0, len(courses), batch_size):
            course_batch = courses[i : i + batch_size]
            futures.append(executor.submit(add_course_embedding, vo, course_batch))

        try:
            for _ in tqdm.tqdm(
                as_completed(futures), desc="Embedding courses", total=len(futures)
            ):
                pass
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Shutting down...")
            for f in futures:
                f.cancel()

            executor.shutdown(wait=False)


def load_course_data(csv_file_path: str) -> list[Course]:
    courses: list[Course] = []
    with open(csv_file_path, encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            course = Course(
                description=row["description"].strip(),
                number=row["number"].strip(),
                title=row["title"].strip(),
                units=row["units"].strip(),
                required_courses=[
                    value
                    for i in range(20)
                    if (value := row[f"requiredCourses[{i}]"].strip())
                ],
                course_objectives=[
                    value.lstrip("\ufe63").strip()
                    for i in range(16)
                    if (value := row[f"courseObjectives[{i}]"].strip())
                ],
                student_learning_outcomes=[
                    value
                    for i in range(24)
                    if (value := row[f"studentLearningOutcomes[{i}]"].strip())
                ],
            )
            courses.append(course)
    return courses


def parse_csv_to_mongodb(
    csv_file_path, mongo_connection_uri, database_name, collection_name
):
    load_dotenv()
    client = MongoClient(mongo_connection_uri)
    collection = client[database_name][collection_name]

    courses = load_course_data(csv_file_path)

    add_course_embeddings(courses, 20)

    collection.insert_many([course.model_dump() for course in courses])

    search_index_model = SearchIndexModel(
        definition={
            "fields": [
                {
                    "type": "vector",
                    "path": "embedding",
                    "numDimensions": 1024,
                    "similarity": "dotProduct",
                }
            ]
        },
        name="vector_index",
        type="vectorSearch",
    )
    collection.create_search_index(search_index_model)

    print("Data successfully inserted into MongoDB")


if __name__ == "__main__":
    csv_file_path = "bt_courses.csv"
    mongo_connection_uri = "mongodb+srv://rathodvikram44:rathodvikram44@allcourses.l4lqk7e.mongodb.net/?retryWrites=true&w=majority&appName=allCourses"
    database_name = "allcourses"
    collection_name = "allcourses_with_embedding"

    parse_csv_to_mongodb(
        csv_file_path, mongo_connection_uri, database_name, collection_name
    )
