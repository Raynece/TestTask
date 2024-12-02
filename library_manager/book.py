class Book:
    """Класс, представляющий книгу."""

    def __init__(self, title: str, author: str, year: int, id: int = None, status: str = "в наличии"):
        self.id = id  # ID может быть передан или установлен позже
        self.title = title
        self.author = author
        self.year = year
        self.status = status  # Теперь статус также передается в конструктор

    def __repr__(self):
        return f"ID: {self.id}, Title: {self.title}, Author: {self.author}, Year: {self.year}, Status: {self.status}"
