from django.http import HttpRequest, HttpResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect
from django.utils.html import escape
from django.views.decorators.http import require_POST

from courses import find_course_by_id, find_user_by_id, mark_theme_completed
from homepage.data import (
    get_session_user_id,
    load_all,
    save_progress,
)
from homepage.views import not_found, page


def course_list(request: HttpRequest) -> HttpResponse:
    courses, _, _ = load_all()
    items = ""
    for course in courses:
        items += (
            '<li class="list-group-item">'
            f'<a href="/courses/{course.id}/">{escape(course.name)}</a>'
            f" – тем: {len(course.themes)}"
            "</li>"
        )
    content = f"""
    <h1>Курсы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page(request, "Трекер – курсы", content))


def course_detail(request: HttpRequest, course_id: int) -> HttpResponse:
    courses, users, _ = load_all()
    course = find_course_by_id(courses, course_id)
    if course is None:
        return not_found(
            request, "Курс не найден", "/courses/", "← к списку курсов"
        )

    user_id = get_session_user_id(request)
    user = find_user_by_id(users, user_id) if user_id is not None else None
    progress = user.get_progress(course.id) if user is not None else None

    items = ""
    for theme in course.themes:
        badge = ""
        if progress is not None and progress.is_theme_completed(theme):
            badge = '<span class="badge bg-success">пройдена</span>'
        items += (
            '<li class="list-group-item d-flex justify-content-between">'
            f'<a href="/courses/{course.id}/themes/{theme.id}/">'
            f"{escape(theme.name)}</a>{badge}</li>"
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(course.name)}</h5>
            <p class="card-text"><strong>ID:</strong> {course.id}</p>
            <p class="card-text">Темы курса:</p>
            <ul class="list-group mb-3">{items}</ul>
            <a href="/courses/" class="btn btn-outline-secondary">
                ← к списку курсов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(request, course.name, content))


def theme_detail(
    request: HttpRequest, course_id: int, theme_id: int
) -> HttpResponse:
    courses, users, progresses = load_all()
    course = find_course_by_id(courses, course_id)
    if course is None:
        return not_found(
            request, "Курс не найден", "/courses/", "← к списку курсов"
        )
    theme = course.get_theme_by_id(theme_id)
    if theme is None:
        return not_found(
            request,
            "Тема не найдена",
            f"/courses/{course.id}/",
            "← к курсу",
        )

    names = [
        escape(progress.user.name)
        for progress in progresses
        if progress.course.id == course.id
        and progress.is_theme_completed(theme)
    ]
    completed_by = ", ".join(names) if names else "никто"

    user_id = get_session_user_id(request)
    user = find_user_by_id(users, user_id) if user_id is not None else None
    if user is None:
        action = (
            '<p class="text-muted">'
            '<a href="/login/">Войдите</a>, чтобы отмечать темы.</p>'
        )
    else:
        progress = user.get_progress(course.id)
        if progress is not None and progress.is_theme_completed(theme):
            action = (
                '<p><span class="badge bg-success">'
                "Вы прошли тему</span></p>"
            )
        else:
            action = f"""
            <form method="post" class="mb-3"
                  action="/courses/{course.id}/themes/{theme.id}/complete/">
                <input type="hidden" name="csrfmiddlewaretoken"
                       value="{get_token(request)}">
                <button type="submit" class="btn btn-success">
                    Отметить пройденной
                </button>
            </form>
            """
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{escape(theme.name)}</h5>
            <p class="card-text">Курс: {escape(course.name)}</p>
            <p class="card-text">{escape(theme.content)}</p>
            <p class="card-text">Прошли тему: {completed_by}</p>
            {action}
            <a href="/courses/{course.id}/"
               class="btn btn-outline-secondary">
                ← к курсу
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(request, theme.name, content))


@require_POST
def theme_complete(
    request: HttpRequest, course_id: int, theme_id: int
) -> HttpResponse:
    """Отметить тему пройденной для вошедшего студента."""
    user_id = get_session_user_id(request)
    if user_id is None:
        return redirect("/login/")
    courses, users, progresses = load_all()
    user = find_user_by_id(users, user_id)
    if user is None:
        request.session.flush()
        return redirect("/login/")
    course = find_course_by_id(courses, course_id)
    if course is None:
        return not_found(
            request, "Курс не найден", "/courses/", "← к списку курсов"
        )
    theme = course.get_theme_by_id(theme_id)
    if theme is None:
        return not_found(
            request,
            "Тема не найдена",
            f"/courses/{course.id}/",
            "← к курсу",
        )

    mark_theme_completed(user, course, theme.name, progresses)
    save_progress(progresses)
    return redirect(f"/courses/{course.id}/themes/{theme.id}/")
