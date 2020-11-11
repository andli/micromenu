#!/usr/bin/env python3
"""
A very lightweight console menu.
"""

__author__ = "Andreas Ehrlund"
__version__ = "1.1.0"
__license__ = "MIT"

import sys

PADDING = 2
MIN_WIDTH = 32
DELIMITER = ":"
TITLE_INDENT = 3


class Menu:
    def __init__(
        self,
        menu_title,
        message_top="",
        message_bottom="",
        min_width=MIN_WIDTH,
        cycle=True,
    ):
        if not menu_title:
            raise ValueError("Menu title required")

        self.cycle = cycle
        self.min_width = min_width
        self.menu_title = menu_title
        self.message_top = message_top
        self.message_bottom = message_bottom
        self.menu_items = []

    def add_function_item(self, item_title, func_ref, kwargs):
        self.menu_items.append((item_title, func_ref, kwargs))

    def show(self):
        self.print_menu()

        while True:
            try:
                choice = int(input("Action number: "))
            except ValueError:
                print("Incorrect input, try again.")
                continue

            if 0 == choice:
                return True
                # yield
            elif choice in range(len(self.menu_items) + 1):
                func = self.menu_items[choice - 1][1]
                kwargs = self.menu_items[choice - 1][2]
                func(**kwargs)
                if self.cycle:
                    self.show()
                return False

            else:
                print("Choose a valid item.")

    def get_total_menu_width(self):
        lengths = [
            len((f"{str(ind)}{DELIMITER} {item[0]}"))
            for ind, item in enumerate(self.menu_items)
        ]
        lengths.append(TITLE_INDENT + len(self.menu_title))

        if self.message_top:
            lengths.append(len(self.message_top))
        if self.message_bottom:
            lengths.append(len(self.message_bottom))

        # +4 for border and padding
        return max(max(lengths) + 4, self.min_width)

    def print_menu(self):

        total_menu_width = self.get_total_menu_width()

        menu_top_left = f"╭{TITLE_INDENT*'─'} {self.menu_title} "
        menu_top_right = "╮"
        menu_top_padding = (
            total_menu_width - len(menu_top_left) - len(menu_top_right)
        ) * "─"
        menu_top = f"{menu_top_left}{menu_top_padding}{menu_top_right}"
        print(menu_top)

        # Top message

        if self.message_top:
            print(self.menu_item_string(self.message_top, total_menu_width))
            print("╞" + (total_menu_width - 2) * "═" + "╡")

        # Menu items

        index = 1
        for item in self.menu_items:
            print(self.menu_item_string(item[0], total_menu_width, index))
            index += 1

        print(self.menu_item_string("Exit", total_menu_width, 0))

        # Bottom message

        if self.message_bottom:
            print("├" + (total_menu_width - 2) * "─" + "┤")
            print(self.menu_item_string(self.message_bottom, total_menu_width))

        print("╰" + (total_menu_width - 2) * "─" + "╯")

    def menu_item_string(self, title, total_menu_width, item_no=None):
        index = ""
        if isinstance(item_no, int):
            index = f"{str(item_no)}{DELIMITER} "
        string_left = f"│ {index}{title} "
        string_right = f"│"
        padding_length = total_menu_width - len(string_left) - len(string_right)
        return f"{string_left}{padding_length * ' '}{string_right}"
