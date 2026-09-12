import json


def load_courses(filename: str) -> dict[int, dict]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            raw_courses = json.load(file)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден, начинаем с пустого списка.")
        return {}
    except json.JSONDecodeError:
        print(f"Файл '{filename}' повреждён, начинаем с пустого списка.")
        return {}

    return {
        int(course_id): course for course_id, course in raw_courses.items()
    }


def save_courses(filename: str, courses: dict[int, dict]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(courses, file, ensure_ascii=False, indent=2)
