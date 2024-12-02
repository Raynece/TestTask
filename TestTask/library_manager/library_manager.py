from book import Book
import utils


class Library:
    """Класс, представляющий библиотеку."""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.books = self.load_books()

    def load_books(self):
        """Загружает книги из файла."""
        books_data = utils.load_books_from_file(self.data_file)
        books = [Book(title=book.title, author=book.author, year=book.year, id=book.id) for book in books_data]
        return books

    def save_books(self):
        """Сохраняет книги в файл."""
        books_data = [book.__dict__ for book in self.books]
        utils.save_books_to_file(self.data_file, books_data)

    def add_book(self, title: str, author: str, year: int):
        """Добавляет книгу в библиотеку."""
        new_book = Book(title, author, year)
        new_book.id = utils.generate_unique_id(self.books)
        self.books.append(new_book)
        self.save_books()

    def remove_book(self, book_id: int):
        """Удаляет книгу по ID."""
        book_to_remove = self.find_book_by_id(book_id)
        if not book_to_remove:
            return None  # Возвращаем None, если книга не найдена
        self.books.remove(book_to_remove)
        self.save_books()
        return book_to_remove

    def find_book_by_id(self, book_id: int):
        """Ищет книгу по ID."""
        return next((book for book in self.books if book.id == book_id), None)

    def search_books(self, query: str):
        """Ищет книги по названию, автору или году."""
        return [book for book in self.books if query.lower() in book.title.lower() or
                query.lower() in book.author.lower() or query in str(book.year)]

    def change_status(self, book_id: int, new_status: str):
        """Меняет статус книги."""
        if new_status not in ["в наличии", "выдана"]:
            raise ValueError("Неверный статус, допустимы: 'в наличии', 'выдана'")

        book = self.find_book_by_id(book_id)
        if not book:
            return None  # Если книга не найдена, возвращаем None
        book.status = new_status
        self.save_books()
        return book

    def show_books(self):
        """Отображает все книги в библиотеке."""
        for book in self.books:
            print(book)


def menu():
    """Меню программы."""
    library = Library("data/library_data.json")

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите опцию: ")

        if choice == "1":
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания книги: "))
            library.add_book(title, author, year)
            print("Книга добавлена!")

        elif choice == "2":
            book_id = input("Введите ID книги, которую хотите удалить: ")
            try:
                book_id = int(book_id)
                book = library.remove_book(book_id)
                if book:
                    print(f"Книга '{book.title}' удалена!")
                else:
                    print(f"Книга с ID {book_id} не найдена.")
            except ValueError:
                print("Ошибка: Введите корректный числовой ID.")

        elif choice == "3":
            query = input("Введите запрос для поиска (по названию, автору или году): ")
            results = library.search_books(query)
            if results:
                print("\nРезультаты поиска:")
                for book in results:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == "4":
            library.show_books()

        elif choice == "5":
            book_id = input("Введите ID книги для изменения статуса: ")
            try:
                book_id = int(book_id)
                new_status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                book = library.change_status(book_id, new_status)
                if book:
                    print(f"Статус книги '{book.title}' изменен на '{new_status}'!")
                else:
                    print(f"Книга с ID {book_id} не найдена.")
            except ValueError as e:
                print(e)  # В случае ошибки, выводим сообщение с ошибкой

        elif choice == "6":
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    menu()
