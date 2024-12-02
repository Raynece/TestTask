import json
import os
from typing import List
from book import Book

def load_books_from_file(file_path: str) -> List[Book]:
    """Загружает книги из JSON-файла и преобразует их в объекты Book."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            books_data = json.load(f)
            # Преобразуем каждый словарь обратно в объект Book, передаем все поля
            return [Book(**book) for book in books_data]
    return []


def save_books_to_file(file_path: str, books: List[Book]):
    """Сохраняет книги в файл в формате JSON."""
    # Если книга является объектом типа Book, используем book.__dict__ для получения данных
    books_data = [book.__dict__ if isinstance(book, Book) else book for book in books]

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)


def generate_unique_id(books: List[Book]) -> int:
    """Генерирует уникальный ID для книги."""
    if books:
        return max(book.id for book in books) + 1
    return 1
