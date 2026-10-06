"""Загрузка данных предметной области ПР3 для веб-страниц."""

from django.conf import settings
from django.http import HttpRequest

from courses import find_user_by_id
from models import Course, Progress, User
from storage import (
    load_courses,
    load_progresses,
    load_users,
    save_progresses,
)

SESSION_KEY = "user_id"


def load_all() -> tuple[list[Course], list[User], list[Progress]]:
    """Загрузить курсы, пользователей и прогресс из каталога data/."""
    courses = load_courses(str(settings.DATA_DIR / "courses.json"))
    users = load_users(str(settings.DATA_DIR / "users.json"))
    progresses = load_progresses(
        str(settings.DATA_DIR / "progress.json"),
        users,
        courses,
    )
    return courses, users, progresses


def save_progress(progresses: list[Progress]) -> None:
    """Сохранить прогресс в data/progress.json."""
    save_progresses(str(settings.DATA_DIR / "progress.json"), progresses)


def get_session_user_id(request: HttpRequest) -> int | None:
    """Вернуть id вошедшего студента из сессии (или None)."""
    user_id = request.session.get(SESSION_KEY)
    if isinstance(user_id, int):
        return user_id
    return None


def get_current_user(request: HttpRequest) -> User | None:
    """Вернуть вошедшего студента без загрузки курсов и прогресса."""
    user_id = get_session_user_id(request)
    if user_id is None:
        return None
    users = load_users(str(settings.DATA_DIR / "users.json"))
    return find_user_by_id(users, user_id)
