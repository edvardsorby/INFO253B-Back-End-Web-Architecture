def individual_serial(course) -> dict:
    return {
        "id": str(course["_id"]),
        "number": course["number"],
        "title": course["title"],
        "description": course["description"],
        "number": course["number"],
        "units": course["units"],
        "required_courses": course["required_courses"],
        "course_objectives": course["course_objectives"],
        "student_learning_outcomes": course["student_learning_outcomes"]
    }

def list_serial(courses) -> list:
    return [individual_serial(course) for course in courses]