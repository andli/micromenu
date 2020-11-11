import pytest
import mock
import builtins
from unittest.mock import patch
from unittest.mock import MagicMock
from io import StringIO

from micromenu import micromenu

# pytest --cov=micromenu --cov-report xml:cov.xml tests/
# pytest --cov=micromenu tests/


class TestMenu:
    def test_add_function_item(self):
        menu = micromenu.Menu(
            "test", "test messsage top", "test message bottom", min_width=20
        )
        assert len(menu.menu_items) == 0
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        assert len(menu.menu_items) == 1

    def test_print_menu(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        menu.print_menu()
        captured = capsys.readouterr()
        assert captured.out.startswith("╭─── test ")

    def test_inputs(self):
        with pytest.raises(ValueError) as excinfo:
            menu = micromenu.Menu("")

        menu = micromenu.Menu("test_title", "")
        assert isinstance(menu, micromenu.Menu)

    def test_dynamic_width(self, capsys):
        overflow = 4

        # test menu title longest
        menu = micromenu.Menu("X" * (micromenu.MIN_WIDTH + overflow), "x")
        menu.add_function_item("x", lambda x: len(x), {"x": "testparam"})
        menu.print_menu()
        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        del lines[-1]
        assert all(len(x) == len(lines[0]) for x in lines)

        # test top menu message longest
        menu = micromenu.Menu("x", "X" * (micromenu.MIN_WIDTH + overflow))
        menu.add_function_item("x", lambda x: len(x), {"x": "testparam"})
        menu.print_menu()
        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        del lines[-1]
        assert all(len(x) == len(lines[0]) for x in lines)

        # test bottom menu message longest
        menu = micromenu.Menu("x", "", "X" * (micromenu.MIN_WIDTH + overflow))
        menu.add_function_item("x", lambda x: len(x), {"x": "testparam"})
        menu.print_menu()
        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        del lines[-1]
        assert all(len(x) == len(lines[0]) for x in lines)

        # test menu item longest
        menu = micromenu.Menu("x", "x")
        menu.add_function_item(
            "X" * (micromenu.MIN_WIDTH + overflow), lambda x: len(x), {"x": "testparam"}
        )
        menu.print_menu()
        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        del lines[-1]
        assert all(len(x) == len(lines[0]) for x in lines)

    def test_invalid_input(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})

        with patch("sys.stdin", StringIO("a\n0")):
            menu.show()
        captured = capsys.readouterr()
        assert "Incorrect input, try again." in captured.out

    def test_menu_item_out_of_range(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})

        with patch("sys.stdin", StringIO("9\n0")):
            menu.show()
        captured = capsys.readouterr()
        assert "Choose a valid item." in captured.out

    def test_menu_item_function_called(self, capsys):
        dummy = MagicMock()

        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", dummy, {"x": "testparam"})

        with patch("sys.stdin", StringIO("1\n0\n0")):
            menu.show()
            assert dummy.called

    def test_menu_terminates(self, capsys):
        menu = micromenu.Menu("test", cycle=False)
        menu.add_function_item("title1", lambda x: print(x), {"x": "done"})

        with patch("sys.stdin", StringIO("0\n0")):
            assert menu.show() == True
