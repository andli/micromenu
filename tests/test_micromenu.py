import pytest

from micromenu import micromenu

#pytest --cov=micromenu --cov-report xml:cov.xml tests/

class TestMenu:
    def test_add_function_item(self):
        menu = micromenu.Menu("test", "test1")
        assert len(menu.menu_items) == 0
        menu.add_function_item("title1", lambda x: len(x), {'x':"testparam"})
        assert len(menu.menu_items) == 1

