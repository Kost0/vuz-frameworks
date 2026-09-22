class Theme:
    """Тема учебного курса."""

    def __init__(self, theme_id: int, name: str) -> None:
        self.id = theme_id
        self.name = name

    def __str__(self) -> str:
        return f"{self.id}. {self.name}"

    @classmethod
    def from_data(cls, data: dict) -> "Theme":
        return cls(theme_id=int(data["id"]), name=data["name"])

    def to_data(self) -> dict:
        return {"id": self.id, "name": self.name}
