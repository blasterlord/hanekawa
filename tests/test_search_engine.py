from unittest import TestCase
from core.search_engine import SearchEngine


class TestSearchEngine(TestCase):
    def setUp(self) -> None:
        self.search_engine = SearchEngine()


class TestInit(TestSearchEngine):
    def test_init(self):
        pass
