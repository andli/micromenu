import re

from io import StringIO
from unittest.mock import MagicMock, patch

from micromenu import micromenu

# pytest --cov=micromenu --cov-report xml:coverage.xml tests/
# pytest --cov=micromenu tests/


class TestMenu:
    def test_add_function_item(self):
        menu = micromenu.Menu(
            "test", "test messsage top", "test message bottom", min_width=20
        )
        assert len(menu.menu_items) == 0
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        assert len(menu.menu_items) == 1

    def test_add_divider(self):
        menu = micromenu.Menu(
            "test", "test messsage top", "test message bottom", min_width=20
        )
        assert len(menu.menu_items) == 0
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        menu.add_divider()
        menu.add_function_item("title2", lambda x: len(x), {"x": "testparam"})
        assert len(menu.menu_items) == 3

    def test_no_top_message(self, capsys):
        menu = micromenu.Menu("test")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        assert len(menu.menu_items) == 1
        menu.print_menu()
        captured = capsys.readouterr()
        assert "╞" not in captured.out

    def test_no_bottom_message(self, capsys):
        menu = micromenu.Menu("test")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        # menu.add_message_bottom_row("hej")
        assert len(menu.menu_items) == 1
        menu.print_menu()
        captured = capsys.readouterr()
        # check for not having a divider right before the exit option
        r = re.search(r"├", captured.out)
        assert r == None

    def test_add_message_bottom_item_no_init(self):
        menu = micromenu.Menu("test", "test messsage top", min_width=20)
        assert len(menu.menu_items) == 0
        menu.add_message_bottom_row("test message bottom")
        assert len(menu.message_bottom) == 1

    def test_add_message_bottom_item_with_init(self):
        menu = micromenu.Menu(
            "test", "test messsage top", "test message bottom", min_width=20
        )
        assert len(menu.menu_items) == 0
        menu.add_message_bottom_row("test message bottom 2")
        menu.add_message_bottom_row("test message bottom 3")
        assert len(menu.message_bottom) == 3

    def test_print_menu(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})
        menu.add_divider()
        menu.add_function_item("title2", lambda x: len(x), {"x": "testparam"})
        menu.print_menu()
        captured = capsys.readouterr()
        assert captured.out.startswith("╭─── test ")

    def test_inputs(self):
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
        menu.add_message_bottom_row("notlongest")
        menu.print_menu()
        captured = capsys.readouterr()
        lines = captured.out.split("\n")
        del lines[-1]
        assert all(len(x) == len(lines[0]) for x in lines)

        # test menu item longest
        def test_item_indexes(num_menu_items):
            menu = micromenu.Menu("x", "x")
            for i in range(num_menu_items):
                menu.add_function_item(
                    "X" * (micromenu.MIN_WIDTH + overflow),
                    lambda x: len(x),
                    {"x": "testparam"},
                )
            menu.print_menu()
            captured = capsys.readouterr()
            lines = captured.out.split("\n")
            del lines[-1]
            assert all(len(x) == len(lines[0]) for x in lines)

        test_item_indexes(9)
        test_item_indexes(10)
        test_item_indexes(11)

    def test_string_uid_input(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item(
            "title1", lambda x: print(x), {"x": "testparam"}, uid="xxx"
        )

        with patch("sys.stdin", StringIO("xxx\n0\n")):
            menu.show()
            captured = capsys.readouterr()
            assert "testparam" in captured.out

    def test_menu_item_out_of_range(self, capsys):
        menu = micromenu.Menu("test", "test messsage top", "test message bottom")
        menu.add_function_item("title1", lambda x: len(x), {"x": "testparam"})

        with patch("sys.stdin", StringIO("9\n0")):
            menu.show()
            captured = capsys.readouterr()
            assert "Invalid number, please try again." in captured.out

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
