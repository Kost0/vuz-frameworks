"""Маршрутизация верхнего уровня: приложения подключаются через include()."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("", include("accounts.urls")),
    path("courses/", include("catalog.urls")),
    path("progress/", include("progress.urls")),
]

handler404 = "homepage.views.page_not_found"
