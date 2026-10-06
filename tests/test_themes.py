import json
from pathlib import Path

import pytest
from django.test import Client

from models import Course, Theme
from storage import load_courses, save_courses

THEME_URL = "/courses/1/themes/2/"
COMPLETE_URL = "/courses/1/themes/2/complete/"


@pytest.fixture
def client() -> Client:
    return Client()


def test_theme_content_defaults_and_roundtrip():
    assert Theme(1, "A").content == ""
    theme = Theme(1, "A", "Текст темы")
    restored = Theme.from_data(theme.to_data())
    assert restored.content == "Текст темы"
    assert Theme.from_data({"id": 1, "name": "A"}).content == ""


def test_save_and_load_courses_keep_theme_content(tmp_path: Path):
    course = Course(1, "Python", [Theme(1, "A", "Текст A")])
    path = str(tmp_path / "courses.json")
    save_courses(path, [course])
    loaded = load_courses(path)
    assert loaded[0].themes[0].content == "Текст A"
    assert loaded[0].themes[0].id == 1


def test_data_files_have_content_for_every_theme(temp_data_dir: Path):
    courses = load_courses(str(temp_data_dir / "courses.json"))
    assert courses
    assert all(theme.content for c in courses for theme in c.themes)


def test_theme_page_shows_content(client: Client):
    html = client.get("/courses/1/themes/1/").content.decode()
    assert "Переменная хранит значение" in html


def test_theme_page_for_guest_suggests_login(client: Client):
    html = client.get(THEME_URL).content.decode()
    assert "Войдите" in html
    assert "Отметить пройденной" not in html


def test_complete_requires_login(client: Client):
    response = client.post(COMPLETE_URL)
    assert response.status_code == 302
    assert response["Location"] == "/login/"


def test_complete_rejects_get(client: Client):
    client.post("/login/", {"name": "Студент"})
    assert client.get(COMPLETE_URL).status_code == 405


def test_mark_theme_creates_progress_for_new_course(
    client: Client, temp_data_dir: Path
):
    client.post("/login/", {"name": "Анна"})
    client.post("/courses/1/themes/1/complete/")
    saved = json.loads((temp_data_dir / "progress.json").read_text("utf-8"))
    assert len(saved) == 3
    assert saved[2]["user_id"] == 2
    assert saved[2]["course_id"] == 1
    assert saved[2]["completed_theme_ids"] == [1]
    assert "прогресс: 20%" in client.get("/my/").content.decode()


@pytest.mark.parametrize(
    "url",
    ["/courses/999/themes/1/complete/", "/courses/1/themes/999/complete/"],
)
def test_complete_missing_objects_return_404(client: Client, url: str):
    client.post("/login/", {"name": "Студент"})
    assert client.post(url).status_code == 404
