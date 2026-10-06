import pytest
from django.test import Client

from courses import find_user_by_id, find_user_by_name
from models import User


@pytest.fixture
def client() -> Client:
    return Client()


def test_find_user_by_name_ignores_case_and_spaces():
    users = [User(1, "Студент", "s@example.com"), User(2, "Анна", "a@e.com")]
    assert find_user_by_name(users, "  анна ") is users[1]
    assert find_user_by_name(users, "Нет такого") is None


def test_find_user_by_id():
    users = [User(1, "Студент", "s@example.com")]
    assert find_user_by_id(users, 1) is users[0]
    assert find_user_by_id(users, 999) is None


def test_login_page_is_available(client: Client):
    response = client.get("/login/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="name"' in html
    assert "Доступные студенты" in html


def test_login_redirects_to_my_courses_and_shows_name(client: Client):
    response = client.post("/login/", {"name": "Анна"})
    assert response.status_code == 302
    assert response["Location"] == "/my/"
    html = client.get("/my/").content.decode()
    assert "Анна" in html
    assert "Разработка на Go" in html
    assert "прогресс: 50%" in html


def test_login_unknown_name_shows_error(client: Client):
    response = client.post("/login/", {"name": "Неизвестный"})
    assert response.status_code == 200
    assert "не найден" in response.content.decode()
    assert client.get("/my/").status_code == 302


def test_my_courses_requires_login(client: Client):
    response = client.get("/my/")
    assert response.status_code == 302
    assert response["Location"] == "/login/"


def test_navigation_shows_login_state(client: Client):
    assert "Войти" in client.get("/").content.decode()
    client.post("/login/", {"name": "Анна"})
    html = client.get("/").content.decode()
    assert "Выйти" in html
    assert "Анна" in html


def test_logout_clears_session(client: Client):
    client.post("/login/", {"name": "Анна"})
    response = client.get("/logout/")
    assert response.status_code == 302
    assert client.get("/my/").status_code == 302
    assert "Войти" in client.get("/").content.decode()
