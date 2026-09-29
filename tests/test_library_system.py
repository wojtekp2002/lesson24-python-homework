import unittest

from src.library_system import Book, Library, Reader


class LibrarySystemTest(unittest.TestCase):
    def setUp(self):
        self.library = Library("Testowa", "Adres 1")
        self.book = Book("Pan Tadeusz", "Adam Mickiewicz", "ISBN-1", 1834)
        self.reader = Reader("Ala", "Nowak", "R001")
        self.library.add_book(self.book)
        self.library.register_reader(self.reader)

    def test_borrow_and_return_book(self):
        self.library.borrow_book("ISBN-1", "R001")

        self.assertFalse(self.book.available)
        self.assertEqual(self.library.reader_loans("R001"), (self.book,))

        self.library.return_book("ISBN-1", "R001")

        self.assertTrue(self.book.available)
        self.assertEqual(self.library.reader_loans("R001"), ())

    def test_search_books_by_title_author_and_isbn(self):
        self.assertEqual(self.library.search_books(title="tadeusz"), [self.book])
        self.assertEqual(self.library.search_books(author="mickiewicz"), [self.book])
        self.assertEqual(self.library.search_books(isbn="ISBN-1"), [self.book])

    def test_encapsulated_collections_are_returned_as_tuples(self):
        self.assertIsInstance(self.library.books, tuple)
        self.assertIsInstance(self.library.readers, tuple)
        self.assertIsInstance(self.reader.borrowed_books, tuple)

    def test_cannot_remove_borrowed_book(self):
        self.library.borrow_book("ISBN-1", "R001")

        with self.assertRaises(ValueError):
            self.library.remove_book("ISBN-1")


if __name__ == "__main__":
    unittest.main()
