from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils.html import escape

from courses import find_user_by_id, find_user_by_name
from homepage.data import SESSION_KEY, get_session_user_id, load_all
from homepage.views import page


def login_view(request: HttpRequest) -> HttpResponse:
    """Вход по имени студента (без пароля)."""
    _, users, _ = load_all()
    error = ""
    if request.method == "POST":
        user = find_user_by_name(users, request.POST.get("name", ""))
        if user is not None:
            request.session[SESSION_KEY] = user.id
            return redirect("/my/")
        error = "Студент с таким именем не найден."

    alert = ""
    if error:
        alert = f'<div class="alert alert-danger">{escape(error)}</div>'
    names = ", ".join(escape(user.name) for user in users)
    content = f"""
    <h1>Вход</h1>
    {alert}
    <form method="post" action="/login/" class="mb-3">
        <input type="hidden" name="csrfmiddlewaretoken"
               value="{get_token(request)}">
        <input type="text" name="name" class="form-control mb-2"
               placeholder="Имя студента" required autofocus>
        <button type="submit" class="btn btn-primary">Войти</button>
    </form>
    <p class="text-muted">Доступные студенты: {names}</p>
    """
    return HttpResponse(page(request, "Вход", content))


def logout_view(request: HttpRequest) -> HttpResponse:
    """Выход: очистка сессии."""
    request.session.flush()
    return redirect("/")


def my_courses(request: HttpRequest) -> HttpResponse:
    """Курсы и прогресс вошедшего студента."""
    user_id = get_session_user_id(request)
    if user_id is None:
        return redirect("/login/")
    courses, users, _ = load_all()
    user = find_user_by_id(users, user_id)
    if user is None:
        request.session.flush()
        return redirect("/login/")

    mine = ""
    others = ""
    for course in courses:
        link = f'<a href="/courses/{course.id}/">{escape(course.name)}</a>'
        progress = user.get_progress(course.id)
        if progress is None:
            others += f'<li class="list-group-item">{link}</li>'
            continue
        mine += (
            '<li class="list-group-item d-flex justify-content-between">'
            f"<span>{link}</span>"
            f'<a href="/progress/{progress.id}/">'
            f"прогресс: {progress.calculate_percent():.0f}%</a></li>"
        )
    if not mine:
        mine = '<li class="list-group-item">Пока нет курсов в работе.</li>'
    content = f"""
    <h1>Мои курсы</h1>
    <p>Студент: {escape(user.name)} ({escape(user.email)})</p>
    <h5>В процессе</h5>
    <ul class="list-group mb-3">{mine}</ul>
    <h5>Другие курсы</h5>
    <ul class="list-group">{others}</ul>
    """
    return HttpResponse(page(request, "Мои курсы", content))
