import pytest
from django.test import Client

from courses import find_course_by_id, find_progress_by_id
from homepage.data import load_all
from models import Course, Progress, Theme, User


@pytest.fixture
def client() -> Client:
    return Client()


def test_load_all_returns_linked_objects():
    courses, users, progresses = load_all()
    assert courses and users and progresses
    assert isinstance(courses[0], Course)
    assert isinstance(users[0], User)
    assert isinstance(progresses[0], Progress)
    assert progresses[0].user is users[0]


def test_find_course_by_id():
    course = Course(1, "Python", [Theme(1, "A")])
    assert find_course_by_id([course], 1) is course
    assert find_course_by_id([course], 999) is None


def test_find_progress_by_id():
    user = User(1, "Иван", "ivan@example.com")
    course = Course(1, "Python", [Theme(1, "A")])
    progress = Progress(1, user, course)
    assert find_progress_by_id([progress], 1) is progress
    assert find_progress_by_id([progress], 999) is None


def test_course_get_theme_by_id():
    theme = Theme(1, "A")
    course = Course(1, "Python", [theme])
    assert course.get_theme_by_id(1) is theme
    assert course.get_theme_by_id(999) is None


@pytest.mark.parametrize(
    "url",
    [
        "/",
        "/courses/",
        "/courses/1/",
        "/courses/1/themes/1/",
        "/progress/",
        "/progress/1/",
    ],
)
def test_pages_return_200(client: Client, url: str):
    response = client.get(url)
    assert response.status_code == 200
    assert "<!DOCTYPE html>" in response.content.decode()


def test_course_page_shows_domain_data(client: Client):
    html = client.get("/courses/1/").content.decode()
    assert "Разработка на Python" in html
    assert "Переменные" in html


@pytest.mark.parametrize(
    "url",
    [
        "/courses/999/",
        "/courses/1/themes/999/",
        "/progress/999/",
        "/nonexistent/",
    ],
)
def test_missing_objects_return_404(client: Client, url: str):
    response = client.get(url)
    assert response.status_code == 404
    assert "<!DOCTYPE html>" in response.content.decode()
