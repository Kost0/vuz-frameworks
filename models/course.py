from typing import Iterable

from .theme import Theme


class Course:
    """Учебный курс, состоящий из набора тем."""

    def __init__(
        self,
        course_id: int,
        name: str,
        themes: list[Theme] | None = None,
    ) -> None:
        self.id = course_id
        self.name = name
        self.themes = themes or []

    def add_theme(self, theme: Theme) -> None:
        """Добавить тему в курс."""
        self.themes.append(theme)

    def get_theme(self, theme_name: str) -> Theme | None:
        """Найти тему курса по точному названию."""
        for theme in self.themes:
            if theme.name == theme_name:
                return theme
        return None

    def calculate_progress(self, completed_theme_ids: Iterable[int]) -> float:
        """Рассчитать процент завершения курса."""
        if not self.themes:
            return 0.0
        completed_ids = set(completed_theme_ids)
        completed = sum(theme.id in completed_ids for theme in self.themes)
        return completed / len(self.themes) * 100

    def __str__(self) -> str:
        return f"{self.id}. {self.name} ({len(self.themes)} тем)"

    @classmethod
    def from_data(cls, data: dict) -> "Course":
        themes = [Theme.from_data(theme) for theme in data.get("themes", [])]
        return cls(
            course_id=int(data["id"]),
            name=data["name"],
            themes=themes,
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "themes": [theme.to_data() for theme in self.themes],
        }
