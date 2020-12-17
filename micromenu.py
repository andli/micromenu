#!/usr/bin/env python3
"""
A very lightweight console menu.
"""

__author__ = "Andreas Ehrlund"
__version__ = "2.0.3"
__license__ = "MIT"

import sys
from typing import Text

PADDING = 2
MIN_WIDTH = 32
DELIMITER = ":"
TITLE_INDENT = 3


class MenuItem:
    def __init__(self, item_title, func_ref, kwargs, index, uid=None):
        self.item_title = item_title
        self.func_ref = func_ref
        self.kwargs = kwargs
        self.index = index
        self.uid = uid  # TODO: minimum length and uniqueness check

    def render(self, width):
        string_left = f"│ {str(self.index)}{DELIMITER} {self.item_title} "
        string_right = f"│"
        padding_length = width - len(string_left) - len(string_right)
        print(f"{string_left}{padding_length * ' '}{string_right}")

    def get_length(self):
        return len((f"{str(self.index+1)}{DELIMITER} {self.item_title}"))

    def execute(self):
        func = self.func_ref
        kwargs = self.kwargs
        func(**kwargs)


class TextItem:
    def __init__(self, text):
        self.text = text

    def get_length(self):
        return len(self.text)

    def render(self, width):
        string_left = f"│ {self.text} "
        string_right = f"│"
        padding_length = width - len(string_left) - len(string_right)
        print(f"{string_left}{padding_length * ' '}{string_right}")


class Divider:
    def __init__(self):
        pass

    def render(self, width, type="single"):
        if type == "double":
            print("╞" + (width - 2) * "═" + "╡")
        else:
            print("├" + (width - 2) * "─" + "┤")


class Menu:
    def __init__(
        self,
        menu_title,
        message_top="",
        message_bottom="",
        min_width=MIN_WIDTH,
        cycle=True,
    ):
        self.cycle = cycle
        self.min_width = min_width
        self.menu_title = menu_title
        self.message_top = TextItem(message_top) if message_top else None
        self.menu_items = []
        self.message_bottom = [TextItem(message_bottom)] if message_bottom else []

    def get_menu_items(self):
        return [x for x in self.menu_items if isinstance(x, MenuItem)]

    def add_function_item(self, item_title, func_ref, kwargs, uid=None):
        item_count = len(self.get_menu_items())
        self.menu_items.append(
            MenuItem(item_title, func_ref, kwargs, item_count + 1, uid)
        )

    def add_divider(self):
        self.menu_items.append(Divider())

    def add_message_bottom_row(self, message):
        self.message_bottom.append(TextItem(message))

    def show(self):
        self.print_menu()

        while True:
            choice = input("Action: ")
            try:
                choice = int(choice)
            except:
                pass

            if isinstance(choice, int):
                choice = int(choice)
                if 0 == choice:
                    return True
                    # yield
                elif choice in range(len(self.get_menu_items()) + 1):
                    for menu_item in self.get_menu_items():
                        if menu_item.index == choice:
                            menu_item.execute()
                            if self.cycle:
                                self.show()
                            return False
                else:
                    print("Invalid number, please try again.")

            elif isinstance(choice, str):
                choice = str(choice)
                for menu_item in self.get_menu_items():
                    if menu_item.uid == choice:
                        menu_item.execute()
                        if self.cycle:
                            self.show()
                        return False

    def get_total_menu_width(self):
        lengths = [
            item.get_length()
            for ind, item in enumerate(self.menu_items)
            if isinstance(item, MenuItem)
        ]
        lengths.append(TITLE_INDENT + len(self.menu_title))

        if self.message_top:
            lengths.append(self.message_top.get_length())
        if self.message_bottom:
            lengths.append(max([x.get_length() for x in self.message_bottom]))

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

        if self.message_top and self.message_top.text != "":
            self.message_top.render(total_menu_width)
            top_divider = Divider()
            top_divider.render(total_menu_width, type="double")

        # Menu items

        for item in self.menu_items:
            if isinstance(item, Divider):
                item.render(total_menu_width)
            if isinstance(item, MenuItem):
                item.render(total_menu_width)

        exit_item = TextItem(f"0{DELIMITER} Exit")
        exit_item.render(total_menu_width)

        # Bottom message

        if self.message_bottom:
            print("├" + (total_menu_width - 2) * "─" + "┤")
            for message in self.message_bottom:
                message.render(total_menu_width)

        print("╰" + (total_menu_width - 2) * "─" + "╯")

