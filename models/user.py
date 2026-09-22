class User:
    """Пользователь системы обучения."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.id = user_id
        self.name = name
        self.email = email
        self.progresses = []

    def add_progress(self, progress: "Progress") -> None:
        """Добавить объект прогресса пользователя."""
        self.progresses.append(progress)

    def get_progress(self, course_id: int) -> "Progress | None":
        """Вернуть прогресс пользователя по курсу."""
        for progress in self.progresses:
            if progress.course.id == course_id:
                return progress
        return None

    def __str__(self) -> str:
        return f"{self.id}. {self.name} <{self.email}>"

    @classmethod
    def from_data(cls, data: dict) -> "User":
        return cls(
            user_id=int(data["id"]),
            name=data["name"],
            email=data["email"],
        )

    def to_data(self) -> dict:
        return {"id": self.id, "name": self.name, "email": self.email}
