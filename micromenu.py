#!/usr/bin/env python3
"""
A very lightweight console menu.
"""

__author__ = "Andreas Ehrlund"
__version__ = "1.0.2"
__license__ = "MIT"

import sys

PADDING = 2
MIN_WIDTH = 52


class Menu:
    def __init__(self, menu_title, message_top="", message_bottom="", cycle=True):
        if not menu_title:
            raise ValueError("Menu title required")

        self.cycle = cycle
        self.PADDING = PADDING
        self.MIN_WIDTH = MIN_WIDTH
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
                break
            elif choice in range(len(self.menu_items) + 1):
                func = self.menu_items[choice - 1][1]
                kwargs = self.menu_items[choice - 1][2]
                func(**kwargs)
                if self.cycle:
                    self.show()
                else:
                    print("Exiting.")
                    break
            else:
                print("Choose a valid item.")

    def get_menu_width(self):
        lengths = [len(item[0]) for item in self.menu_items]
        lengths.append(len(self.menu_title))

        if self.message_top:
            lengths.append(len(self.message_top))
        if self.message_bottom:
            lengths.append(len(self.message_bottom))

        return max(self.PADDING + max(lengths), self.MIN_WIDTH)

    def print_menu(self):

        menu_width = self.get_menu_width()

        menu_top_right = (menu_width - len(self.menu_title) - 1) * "─" + "╮"
        menu_top = f"╭─── {self.menu_title} {menu_top_right}"
        print(menu_top)

        if self.message_top:
            menu_message_top_right = (
                menu_width - len(self.message_top) + 2
            ) * " " + "│"
            menu_message_top = f"│ {self.message_top} {menu_message_top_right}"
            print(menu_message_top)
            print("╞" + (menu_width + 4) * "═" + "╡")

        index = 1
        for item in self.menu_items:
            print(
                "│ {}: {}{}│".format(
                    str(index), item[0], (menu_width - len(item[0])) * " "
                )
            )
            index += 1
        print("│ 0: Exit" + (len(menu_top) - 10) * " " + "│")

        if self.message_bottom:
            print("├" + (menu_width + 4) * "─" + "┤")
            menu_message_bottom_right = (
                menu_width - len(self.message_bottom) + 2
            ) * " " + "│"
            menu_message_bottom = f"│ {self.message_bottom} {menu_message_bottom_right}"
            print(menu_message_bottom)

        print("╰" + (len(menu_top) - 2) * "─" + "╯")
