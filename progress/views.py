from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from courses import find_progress_by_id
from homepage.data import load_all
from homepage.views import not_found, page


def progress_list(request: HttpRequest) -> HttpResponse:
    _, _, progresses = load_all()
    items = ""
    for progress in progresses:
        items += (
            '<li class="list-group-item">'
            f'<a href="/progress/{progress.id}/">'
            f"{escape(progress.user.name)}: {escape(progress.course.name)}"
            f"</a> – {progress.calculate_percent():.0f}%"
            "</li>"
        )
    content = f"""
    <h1>Прогресс</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page(request, "Трекер – прогресс", content))


def progress_detail(
    request: HttpRequest, progress_id: int
) -> HttpResponse:
    _, _, progresses = load_all()
    progress = find_progress_by_id(progresses, progress_id)
    if progress is None:
        return not_found(
            request,
            "Прогресс не найден",
            "/progress/",
            "← к списку прогресса",
        )

    items = ""
    for theme in progress.course.themes:
        done = progress.is_theme_completed(theme)
        status = "пройдена" if done else "не пройдена"
        badge = "bg-success" if done else "bg-secondary"
        items += (
            '<li class="list-group-item d-flex justify-content-between">'
            f"{escape(theme.name)}"
            f'<span class="badge {badge}">{status}</span></li>'
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Прогресс №{progress.id}</h5>
            <p class="card-text">
                Пользователь: {escape(progress.user.name)}
                ({escape(progress.user.email)})
            </p>
            <p class="card-text">
                Курс:
                <a href="/courses/{progress.course.id}/">
                    {escape(progress.course.name)}
                </a>
            </p>
            <p class="card-text">
                Пройдено: {progress.calculate_percent():.0f}%
            </p>
            <ul class="list-group mb-3">{items}</ul>
            <a href="/progress/" class="btn btn-outline-secondary">
                ← к списку прогресса
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(request, f"Прогресс №{progress.id}", content)
    )
