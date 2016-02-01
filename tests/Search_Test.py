from nose.tools import *
from vii.Search import *
from vii.Buffer import *

class SearchResult_Test:
    def test_(self):
        result = SearchResult()
        result.position = Position(2, 2)
        result.string = "Hello"
        assert str(result) == "2,2:'Hello'"

class Search_Test:

    def setup(self):
        self.fixture = Search()
        self.buffer = Buffer()
        self.fixture.buffer = self.buffer

    def test_init(self):
        assert self.fixture.__class__ == Search
        self.buffer.fill("hello\n")
        assert self.fixture.buffer.__str__() == "hello\n"

    def test_search_in_line(self):
        prefill = "\naa b aa b aa b\n"
        self.buffer.fill(prefill)
        pattern = r"aa"
        range = Range(2)
        results = self.fixture.search(pattern, range)
        assert len(results) == 3
        assert results[1].string == "aa"
        assert results[1].position == Position(2,6)

    def test_search_in_lines(self):
        prefill = "\naa b aa b aa b\n\naa b aa b\n"
        self.buffer.fill(prefill)
        pattern = r"aa"
        range = Range(2, 4)
        results = self.fixture.search(pattern, range)
        assert len(results) == 5
        assert results[1].string == "aa"
        assert results[1].position == Position(2,6)
        assert results[4].string == "aa"
        assert results[4].position == Position(4,6)

    def test_search_word_in_line(self):
        prefill = "\naa  bb..cc\n"
        self.buffer.fill(prefill)
        pattern = r"\w+"
        range = Range(2)
        results = self.fixture.search(pattern, range)
        assert len(results) == 3
        assert str(results[0]) == "aa"
        assert str(results[1]) == "bb"
        assert str(results[2]) == "cc"
        assert results[0].position == Position(2,1)
        assert results[1].position == Position(2,5)
        assert results[2].position == Position(2,9)

    def test_search_with_limit(self):
        prefill = "\naa b aa b aa b\naa b aa bn\naa b aa b\n"
        self.buffer.fill(prefill)
        pattern = r"aa"
        range = Range(2, 4)
        results = self.fixture.search(pattern, range, 4)
        assert len(results) == 4

    def test_search_word(self):
        prefill = "\n22 22 22\n  33 33 \n"
        self.buffer.fill(prefill)
        pattern = r"\w+"
        range = Range((2,1),(3,1))
        results = self.fixture.search(pattern, range, 1)
        assert str(results) == "[2,1:'22']"
        range = Range((2,2),(3,1))
        results = self.fixture.search(pattern, range, 1)
        assert str(results) == "[2,4:'22']"


