import pytest
from io import StringIO

from micromenu import micromenu

# pytest --cov=micromenu --cov-report xml:cov.xml tests/


class TestMenu:
    def test_add_function_item(self):
        menu = micromenu.Menu("test", "test1")
        assert len(menu.menu_items) == 0
        menu.add_function_item("title1", lambda x: len(x), {'x': "testparam"})
        assert len(menu.menu_items) == 1

    def test_print_menu(self, capsys):
        menu = micromenu.Menu("test", "test1")
        menu.add_function_item("title1", lambda x: len(x), {'x': "testparam"})
        menu.print_menu(menu.menu_title, menu.message, menu.menu_items)
        captured = capsys.readouterr()
        assert captured.out.startswith("╭─── test ")

    def test_show_menu(self, capsys, monkeypatch):
        menu = micromenu.Menu("test", "test1")
        menu.add_function_item("title1", lambda x: len(x), {'x': "testparam"})
        menu.show()

        with capsys.disabled():
            #monkeypatch.setattr('sys.stdin', io.StringIO('1'))
            monkeypatch.setattr('sys.stdin', io.StringIO('0'))

        captured = capsys.readouterr()
        
