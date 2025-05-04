import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import tqdm
import voyageai
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

from search.models import Course

COURSE_DOC_TEMPLATE = """\
Course Title:
{full_title}

Course Catalog Description:
{catalog_description}

{class_description}"""


def format_course_docs(courses: list[Course]) -> list[tuple[Course, str]]:
    pairs = []
    seen_docs = set()
    for course in courses:
        full_title = (
            f"{course.course_title}\n{course.special_title}"
            if course.special_title
            else course.course_title
        )
        doc = COURSE_DOC_TEMPLATE.format(
            full_title=full_title,
            catalog_description=course.catalog_description,
            class_description=f"Class Description:\n{course.class_description}"
            if course.class_description
            else "",
        )
        key = doc + str(course.term_name)
        if key not in seen_docs:
            pairs.append((course, doc))
            seen_docs.add(key)

    return pairs


def add_course_embedding(
    client: voyageai.Client, batch: list[tuple[Course, str]]
) -> list[float]:
    vectors = client.embed(
        [elem[1] for elem in batch], model="voyage-3-large", input_type="document"
    ).embeddings
    for course, vec in zip([elem[0] for elem in batch], vectors, strict=True):
        course.embedding = vec


def add_course_embeddings(pairs: list[tuple[Course, str]], concurrency: int = 10):
    vo = voyageai.Client()

    batch_size = 128
    with ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = []
        for i in range(0, len(pairs), batch_size):
            batch = pairs[i : i + batch_size]
            futures.append(executor.submit(add_course_embedding, vo, batch))

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


def load_course_data(file_paths: list[str]):
    courses = []
    for file in file_paths:
        with open(file) as f:
            for line in f:
                courses.append(Course(**json.loads(line)))
    return courses


def parse_csv_to_mongodb(
    file_paths, mongo_connection_uri, database_name, collection_name
):
    client = MongoClient(mongo_connection_uri)
    collection = client[database_name][collection_name]

    courses = load_course_data(file_paths)

    pairs = format_course_docs(courses)
    print(f"Removed {len(courses) - len(pairs)} duplicates")

    add_course_embeddings(pairs, 20)

    collection.insert_many([pairs[0].model_dump() for pairs in pairs])

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
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-paths", type=str, nargs="+")
    args = parser.parse_args()

    mongo_connection_uri = os.getenv("MONGO_URI_COURSES")
    database_name = "allcourses"
    collection_name = "allcourses_with_embedding"

    parse_csv_to_mongodb(
        args.data_paths, mongo_connection_uri, database_name, collection_name
    )
