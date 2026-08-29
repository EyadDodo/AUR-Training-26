from abc import ABC, abstractmethod
from enum import Enum


class ItemStatus(Enum):
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"
    LOST = "Lost"


class LibraryItem(ABC):
    _registry = {}

    def __init__(self, title, status=ItemStatus.AVAILABLE):
        self.title = title
        self._status = status

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[cls.__name__] = cls

    @property
    @abstractmethod
    def loan_period(self):
        pass

    @property
    def type(self):
        return self.__class__.__name__

    @property
    def status(self):
        return self._status

    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError(f"'{self.title}' is not available.")
        self._status = ItemStatus.CHECKED_OUT

    def return_item(self):
        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError(f"'{self.title}' is not checked out.")
        self._status = ItemStatus.AVAILABLE

    def mark_lost(self):
        self._status = ItemStatus.LOST

    def __lt__(self, other):
        return self.title.lower() < other.title.lower()

    def __str__(self):
        return f"{self.title} ({self.type}) — {self.status.value}"

    @classmethod
    def from_line(cls, line):
        """Builds an item directly from a simple pipe-separated line."""
        parts = [p.strip() for p in line.strip().split("|")]
        item_type = parts[0]
        subclass = cls._registry.get(item_type)
        if not subclass:
            raise ValueError(f"Unknown type '{item_type}'")
        return subclass._from_parts(parts)

    @staticmethod
    def validate_isbn(isbn):
        isbn = isbn.replace("-", "").replace(" ", "")
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        total = sum(int(x) * (1 if i % 2 == 0 else 3) for i, x in enumerate(isbn[:12]))
        return (10 - total % 10) % 10 == int(isbn[-1])


class Book(LibraryItem):
    def __init__(self, title, author, isbn, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.author = author
        self.isbn = isbn

    @property
    def loan_period(self):
        return 21

    @classmethod
    def _from_parts(cls, parts):
        # Format: Book | title | author | isbn | status
        return cls(parts[1], parts[2], parts[3], ItemStatus[parts[4]])


class DVD(LibraryItem):
    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.director = director

    @property
    def loan_period(self):
        return 5

    @classmethod
    def _from_parts(cls, parts):
        # Format: DVD | title | director | status
        return cls(parts[1], parts[2], ItemStatus[parts[3]])


class Magazine(LibraryItem):
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.issue = issue

    @property
    def loan_period(self):
        return 14

    @classmethod
    def _from_parts(cls, parts):
        # Format: Magazine | title | issue | status
        return cls(parts[1], parts[2], ItemStatus[parts[3]])


class Database:
    """Reads/writes simple pipe-separated lines from database.txt."""

    def __init__(self, filepath="database.txt"):
        self.filepath = filepath

    def load(self):
        items = []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        items.append(LibraryItem.from_line(line))
        except FileNotFoundError:
            return []
        return items

    def save(self, items):
        with open(self.filepath, "w", encoding="utf-8") as f:
            for item in items:
                if isinstance(item, Book):
                    line = f"Book|{item.title}|{item.author}|{item.isbn}|{item.status.name}\n"
                elif isinstance(item, DVD):
                    line = f"DVD|{item.title}|{item.director}|{item.status.name}\n"
                elif isinstance(item, Magazine):
                    line = f"Magazine|{item.title}|{item.issue}|{item.status.name}\n"
                f.write(line)


class Library:
    def __init__(self, database=None):
        self._items = []
        self._database = database

    def load_from_db(self):
        if self._database:
            self._items = self._database.load()

    def save_to_db(self):
        if self._database:
            self._database.save(self._items)

    def add_item(self, item):
        self._items.append(item)

    def checkout(self, title):
        item = self.find_by_title(title)
        if item:
            item.checkout()

    def return_item(self, title):
        item = self.find_by_title(title)
        if item:
            item.return_item()

    def find_by_title(self, title):
        for item in self._items:
            if item.title.lower() == title.lower():
                return item
        return None

    def list_available(self):
        return sorted([item for item in self._items if item.status == ItemStatus.AVAILABLE])