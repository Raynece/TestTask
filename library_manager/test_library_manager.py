import unittest
from library_manager import Library
from book import Book
import os
import json


class TestLibraryManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Этот метод вызывается один раз перед всеми тестами."""
        cls.test_data_file = "data/test_library_data.json"
        cls.library = Library(cls.test_data_file)

    def setUp(self):
        """Этот метод вызывается перед каждым тестом."""
        # Создаем пустой тестовый файл перед каждым тестом
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        self.library.save_books()  # Сохраняем пустой файл для начала

    def tearDown(self):
        """Этот метод вызывается после каждого теста."""
        # Удаляем тестовый файл после каждого теста
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def test_add_book(self):
        """Тестируем добавление книги в библиотеку."""
        self.library.add_book("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997)
        books = self.library.books
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Гарри Поттер и философский камень")
        self.assertEqual(books[0].author, "Дж.К. Роулинг")
        self.assertEqual(books[0].year, 1997)
        self.assertEqual(books[0].status, "в наличии")
        print("Тест 'test_add_book' прошел успешно!")

    def test_remove_book(self):
        """Тестируем удаление книги по ID."""
        # Очищаем библиотеку перед тестом
        self.library.books.clear()

        # Добавляем одну книгу
        self.library.add_book("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997)

        # Проверяем, что в библиотеке одна книга
        self.assertEqual(len(self.library.books), 1)

        # Получаем ID книги для удаления
        book_id = self.library.books[0].id

        # Удаляем книгу
        removed_book = self.library.remove_book(book_id)

        # Проверяем, что книга была удалена
        self.assertEqual(removed_book.id, book_id)
        self.assertEqual(len(self.library.books), 0)  # Проверяем, что список книг пуст

        print("Тест 'test_remove_book' прошел успешно!")

    def test_remove_non_existent_book(self):
        """Тестируем попытку удалить несуществующую книгу."""
        removed_book = self.library.remove_book(999)  # Нет книги с таким ID
        self.assertIsNone(removed_book)
        print("Тест 'test_remove_non_existent_book' прошел успешно!")

    def test_search_books(self):
        """Тестируем поиск книг по запросу."""
        # Очищаем библиотеку и добавляем только нужные книги
        self.library.add_book("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997)
        self.library.add_book("Война и мир", "Лев Толстой", 1869)

        # Поиск по названию книги
        results = self.library.search_books("Гарри Поттер")
        self.assertEqual(len(results), 1)  # Должна быть только одна книга, которая соответствует запросу
        self.assertEqual(results[0].title, "Гарри Поттер и философский камень")

        # Поиск по году издания
        results = self.library.search_books("1869")
        self.assertEqual(len(results), 1)  # Должна быть только одна книга с таким годом
        self.assertEqual(results[0].title, "Война и мир")

        # Поиск по автору
        results = self.library.search_books("Дж.К. Роулинг")
        self.assertEqual(len(results), 1)  # Должна быть только одна книга, написанная этим автором
        self.assertEqual(results[0].title, "Гарри Поттер и философский камень")

        # Поиск по несуществующему запросу
        results = self.library.search_books("Достоевский")  # Книги с этим автором нет
        self.assertEqual(len(results), 0)  # Ничего не найдено

        print("Тест 'test_search_books' прошел успешно!")

    def test_change_status(self):
        """Тестируем изменение статуса книги."""
        self.library.add_book("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997)
        book_id = self.library.books[0].id

        book = self.library.change_status(book_id, "выдана")
        self.assertEqual(book.status, "выдана")

        # Попытка установить неверный статус
        with self.assertRaises(ValueError):
            self.library.change_status(book_id, "неизвестный статус")

        print("Тест 'test_change_status' прошел успешно!")

    def test_show_books(self):
        """Тестируем отображение всех книг."""
        self.library.add_book("Гарри Поттер и философский камень", "Дж.К. Роулинг", 1997)
        self.library.add_book("Война и мир", "Лев Толстой", 1869)

        # Сохраняем список книг в строку
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        self.library.show_books()
        output = sys.stdout.getvalue()

        sys.stdout = old_stdout  # Восстанавливаем стандартный вывод

        self.assertIn("Гарри Поттер и философский камень", output)
        self.assertIn("Война и мир", output)

        print("Тест 'test_show_books' прошел успешно!")

    def test_load_books_from_file(self):
        """Тестируем загрузку книг из файла."""
        test_books = [
            {"id": 1, "title": "Гарри Поттер и философский камень", "author": "Дж.К. Роулинг", "year": 1997,
             "status": "в наличии"},
            {"id": 2, "title": "Война и мир", "author": "Лев Толстой", "year": 1869, "status": "выдана"}
        ]

        # Создаем файл с тестовыми данными
        with open(self.test_data_file, "w", encoding="utf-8") as f:
            json.dump(test_books, f, ensure_ascii=False, indent=4)

        # Загружаем книги из файла
        library = Library(self.test_data_file)
        self.assertEqual(len(library.books), 2)
        self.assertEqual(library.books[0].title, "Гарри Поттер и философский камень")
        self.assertEqual(library.books[1].title, "Война и мир")

        print("Тест 'test_load_books_from_file' прошел успешно!")


if __name__ == "__main__":
    unittest.main()
