from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .course import Course
    from .theme import Theme
    from .user import User


class Progress:
    """Прогресс конкретного пользователя по конкретному курсу."""

    def __init__(
        self,
        progress_id: int,
        user: "User",
        course: "Course",
        completed_theme_ids: list[int] | None = None,
    ) -> None:
        self.id = progress_id
        self.user = user
        self.course = course
        self.completed_theme_ids = set(completed_theme_ids or [])

    def mark_theme_completed(self, theme: "Theme") -> bool:
        """Отметить тему курса пройденной."""
        if theme not in self.course.themes:
            return False
        self.completed_theme_ids.add(theme.id)
        return True

    def is_theme_completed(self, theme: "Theme") -> bool:
        """Проверить, завершена ли тема."""
        return theme.id in self.completed_theme_ids

    def calculate_percent(self) -> float:
        """Вернуть процент прохождения курса."""
        return self.course.calculate_progress(self.completed_theme_ids)

    def __str__(self) -> str:
        return (
            f"{self.user.name}: {self.course.name} — "
            f"{self.calculate_percent():.0f}%"
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user.id,
            "course_id": self.course.id,
            "completed_theme_ids": sorted(self.completed_theme_ids),
        }
