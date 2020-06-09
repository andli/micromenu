#!/usr/bin/env python3
"""
A very lightweight console menu.
"""

__author__ = "Andreas Ehrlund"
__version__ = "0.9.9.2"
__license__ = "MIT"

import sys

PADDING = 2
MIN_WIDTH = 52


class Menu:
    def __init__(self, menu_title, message_top="", message_bottom=""):
        if not menu_title:
            raise ValueError("Menu title required")

        self.PADDING = PADDING
        self.MIN_WIDTH = MIN_WIDTH
        self.menu_title = menu_title
        self.message_top = message_top
        self.message_bottom = message_bottom
        self.menu_items = []

    def add_function_item(self, title, func_ref, kwargs):
        self.menu_items.append((title, func_ref, kwargs))

    def show(self):
        self.print_menu(
            self.menu_title, self.message_top, self.message_bottom, self.menu_items
        )

        while True:
            try:
                choice = int(input("Action number: "))
            except ValueError:
                print("Incorrect input, try again.")
                continue

            if 0 == choice:
                break
            elif choice in range(len(self.menu_items) + 1):
                func = self.menu_items[choice - 1][1]
                kwargs = self.menu_items[choice - 1][2]
                func(**kwargs)
                self.show()
                break
            else:
                print("Choose a valid item.")

    def print_menu(self, title, message_top, message_bottom, menu_items):
        lengths = [len(item[0]) for item in menu_items]
        lengths.extend([len(message_top), len(title)])
        menu_width = max(self.PADDING + max(lengths), self.MIN_WIDTH)
        if message_top:
            menu_width = max(menu_width, len(message_top))
        menu_top_right = (menu_width - len(title) - 1) * "─" + "╮"
        menu_top = f"╭─── {title} {menu_top_right}"
        print(menu_top)

        if message_top:
            menu_message_top_right = (menu_width - len(message_top) + 2) * " " + "│"
            menu_message_top = f"│ {message_top} {menu_message_top_right}"
            print(menu_message_top)
            print("╞" + (menu_width + 4) * "═" + "╡")

        index = 1
        for item in menu_items:
            print(
                "│ {}: {}{}│".format(
                    str(index), item[0], (menu_width - len(item[0])) * " "
                )
            )
            index += 1
        print("│ 0: Exit" + (len(menu_top) - 10) * " " + "│")

        if message_bottom:
            print("├" + (menu_width + 4) * "─" + "┤")
            menu_message_bottom_right = (
                menu_width - len(message_bottom) + 2
            ) * " " + "│"
            menu_message_bottom = f"│ {message_bottom} {menu_message_bottom_right}"
            print(menu_message_bottom)

        print("╰" + (len(menu_top) - 2) * "─" + "╯")
