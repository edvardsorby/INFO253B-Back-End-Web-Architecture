def individual_serial(course) -> dict:
    return {
        "id": str(course["_id"]),
        "url": course["url"],
        "term_name": course["term_name"],
        "department": course["department"],
        "course_number": course["course_number"],
        "section_id": course["section_id"],
        "course_title": course["course_title"],
        "special_title": course["special_title"],
        "instructor": course["instructor"],
        "catalog_description": course["catalog_description"],
        "class_description": course["class_description"],
        "location": course["location"],
        "embedding": course["embedding"],
    }


def list_serial(courses) -> list:
    return [individual_serial(course) for course in courses]
