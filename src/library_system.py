"""Obiektowy system zarządzania biblioteką."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    publication_year: int
    _available: bool = field(default=True, repr=False)

    @property
    def available(self) -> bool:
        return self._available

    def mark_as_borrowed(self) -> None:
        if not self._available:
            raise ValueError("Książka jest już wypożyczona.")
        self._available = False

    def mark_as_returned(self) -> None:
        self._available = True


@dataclass
class Reader:
    first_name: str
    last_name: str
    reader_number: str
    _borrowed_books: list[Book] = field(default_factory=list, repr=False)

    @property
    def borrowed_books(self) -> tuple[Book, ...]:
        return tuple(self._borrowed_books)

    def borrow_book(self, book: Book) -> None:
        if book in self._borrowed_books:
            raise ValueError("Czytelnik ma już tę książkę.")
        self._borrowed_books.append(book)

    def return_book(self, isbn: str) -> Book:
        for book in self._borrowed_books:
            if book.isbn == isbn:
                self._borrowed_books.remove(book)
                return book
        raise ValueError("Czytelnik nie ma książki o podanym ISBN.")


class Library:
    """Biblioteka przechowująca książki i czytelników w enkapsulowanych kolekcjach."""

    def __init__(self, name: str, address: str) -> None:
        self.name = name
        self.address = address
        self._books: dict[str, Book] = {}
        self._readers: dict[str, Reader] = {}

    @property
    def books(self) -> tuple[Book, ...]:
        return tuple(self._books.values())

    @property
    def readers(self) -> tuple[Reader, ...]:
        return tuple(self._readers.values())

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise ValueError("Książka o takim ISBN już istnieje.")
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> bool:
        book = self._books.get(isbn)
        if book is None:
            return False
        if not book.available:
            raise ValueError("Nie można usunąć wypożyczonej książki.")
        del self._books[isbn]
        return True

    def register_reader(self, reader: Reader) -> None:
        if reader.reader_number in self._readers:
            raise ValueError("Czytelnik o takim numerze już istnieje.")
        self._readers[reader.reader_number] = reader

    def remove_reader(self, reader_number: str) -> bool:
        reader = self._readers.get(reader_number)
        if reader is None:
            return False
        if reader.borrowed_books:
            raise ValueError("Nie można usunąć czytelnika z wypożyczonymi książkami.")
        del self._readers[reader_number]
        return True

    def borrow_book(self, isbn: str, reader_number: str) -> None:
        book = self._get_book(isbn)
        reader = self._get_reader(reader_number)
        book.mark_as_borrowed()
        reader.borrow_book(book)

    def return_book(self, isbn: str, reader_number: str) -> None:
        reader = self._get_reader(reader_number)
        book = reader.return_book(isbn)
        book.mark_as_returned()

    def search_books(
        self, title: str | None = None, author: str | None = None, isbn: str | None = None
    ) -> list[Book]:
        results = list(self._books.values())

        if title:
            title = title.lower()
            results = [book for book in results if title in book.title.lower()]
        if author:
            author = author.lower()
            results = [book for book in results if author in book.author.lower()]
        if isbn:
            results = [book for book in results if book.isbn == isbn]

        return results

    def reader_loans(self, reader_number: str) -> tuple[Book, ...]:
        return self._get_reader(reader_number).borrowed_books

    def _get_book(self, isbn: str) -> Book:
        try:
            return self._books[isbn]
        except KeyError as error:
            raise ValueError("Nie znaleziono książki o podanym ISBN.") from error

    def _get_reader(self, reader_number: str) -> Reader:
        try:
            return self._readers[reader_number]
        except KeyError as error:
            raise ValueError("Nie znaleziono czytelnika o podanym numerze.") from error


def build_demo_library() -> Library:
    library = Library("Biblioteka Miejska", "ul. Pythonowa 3")
    library.add_book(Book("Czysty kod", "Robert C. Martin", "9780132350884", 2008))
    library.add_book(Book("Python. Wprowadzenie", "Mark Lutz", "9788328348811", 2018))
    library.add_book(Book("Automate the Boring Stuff", "Al Sweigart", "9781593279929", 2019))
    library.register_reader(Reader("Anna", "Nowak", "R001"))
    library.register_reader(Reader("Jan", "Kowalski", "R002"))
    return library


def main() -> None:
    library = build_demo_library()

    print(f"{library.name} - {library.address}")
    print("\nKolekcja książek:")
    for book in library.books:
        print(f"- {book.title}, {book.author}, ISBN {book.isbn}")

    print("\nWypożyczam książkę czytelnikowi R001...")
    library.borrow_book("9780132350884", "R001")

    print("Wypożyczenia czytelnika R001:")
    for book in library.reader_loans("R001"):
        print(f"- {book.title}")

    print("\nWyniki wyszukiwania po autorze 'Lutz':")
    for book in library.search_books(author="Lutz"):
        print(f"- {book.title} ({book.publication_year})")

    print("\nZwracam książkę...")
    library.return_book("9780132350884", "R001")
    print(f"Liczba wypożyczeń R001: {len(library.reader_loans('R001'))}")


if __name__ == "__main__":
    main()
