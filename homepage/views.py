from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.data import get_current_user

BOOTSTRAP_CSS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
    "/dist/css/bootstrap.min.css"
)


def auth_links(request: HttpRequest) -> str:
    """Ссылки входа/выхода для навигации."""
    user = get_current_user(request)
    if user is None:
        return '<a class="nav-link" href="/login/">Войти</a>'
    return (
        '<a class="nav-link" href="/my/">Мои курсы</a>'
        f'<span class="nav-link disabled">{escape(user.name)}</span>'
        '<a class="nav-link" href="/logout/">Выйти</a>'
    )


def page(request: HttpRequest, title: str, content: str) -> str:
    """Собрать HTML-страницу: кодировка, Bootstrap, навигация."""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{BOOTSTRAP_CSS}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/courses/">Курсы</a>
        <a class="nav-link" href="/progress/">Прогресс</a>
        {auth_links(request)}
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def not_found(
    request: HttpRequest, message: str, back_url: str, back_text: str
) -> HttpResponse:
    """Страница с сообщением об ошибке и кодом статуса 404."""
    content = f"""
    <h1 class="text-danger">{escape(message)}</h1>
    <a href="{back_url}" class="btn btn-outline-secondary">
        {escape(back_text)}
    </a>
    """
    return HttpResponse(page(request, message, content), status=404)


def index(request: HttpRequest) -> HttpResponse:
    content = """
    <h1 class="display-4">Трекер обучения</h1>
    <p class="lead">Курсы, темы и прогресс прохождения.</p>
    <p>Основные разделы:</p>
    <a href="/courses/" class="btn btn-primary me-2">Курсы</a>
    <a href="/progress/" class="btn btn-secondary me-2">Прогресс</a>
    <a href="/my/" class="btn btn-success">Мои курсы</a>
    """
    return HttpResponse(page(request, "Трекер обучения", content))


def page_not_found(
    request: HttpRequest, exception: Exception
) -> HttpResponse:
    """Обработчик handler404: страница не найдена."""
    content = """
    <h1 class="text-danger">404 – страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page(request, "404 – страница не найдена", content),
        status=404,
    )
