import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
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

    def test_invalid_input(self, capsys):
        menu = micromenu.Menu("test", "test1")
        menu.add_function_item("title1", lambda x: len(x), {'x': "testparam"})
        
        with patch('sys.stdin', StringIO("a\n0")):
            menu.show()
        captured = capsys.readouterr()
        assert "Incorrect input, try again." in captured.out
    
    def test_menu_item_out_of_range(self, capsys):
        menu = micromenu.Menu("test", "test1")
        menu.add_function_item("title1", lambda x: len(x), {'x': "testparam"})
        
        with patch('sys.stdin', StringIO("9\n0")):
            menu.show()
        captured = capsys.readouterr()
        assert "Choose a valid item." in captured.out

    def test_menu_item_function_called(self, capsys):
        dummy = MagicMock()

        menu = micromenu.Menu("test", "test1")
        menu.add_function_item("title1", dummy, {'x': "testparam"})
        
        with patch('sys.stdin', StringIO("1\n0")):
            menu.show()

        assert dummy.called


