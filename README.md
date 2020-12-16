# micromenu

![CI and CD](https://github.com/andli/micromenu/workflows/CI%20and%20CD/badge.svg) [![codecov](https://codecov.io/gh/andli/micromenu/branch/master/graph/badge.svg)](https://codecov.io/gh/andli/micromenu) ![PyPI](https://img.shields.io/pypi/v/micromenu) ![PyPI - Downloads](https://img.shields.io/pypi/dm/micromenu)

A minimalistic command line menu for Python, with a title and optional message bars and dividers. Callable functions are attached to each menu item.

```terminal
╭─── This is a title ────────────────────────╮
│ Message that shows on top                  │
╞════════════════════════════════════════════╡
│ 1: Menu item 1                             │
│ 2: Menu item 2                             │
│ 3: Menu item 3                             │
├────────────────────────────────────────────┤
│ 0: Exit                                    │
├────────────────────────────────────────────┤
│ Bottom message row 1                       │
│ Bottom message row 2                       │
╰────────────────────────────────────────────╯
Action number:
```

Set the parameter `cycle=False` if the menu should not loop back after an item has been executed. `menu.show()` will return `True` after terminating.

`add_function_item` has an optional parameter `uid` which can be used to address the menu options without using the index numbers.

## Installation

```bash
python3 -m pip install micromenu
```

## Example usage

```python
import micromenu

menu = micromenu.Menu("test", "this is a message", "and a bottom message", min_width=25)
menu.add_function_item("item1", lambda x: print(x), {'x':"testparam"})
menu.add_divider()
menu.add_function_item("item2", lambda x: print(x), {'x':"testparam"}))
menu.add_message_bottom_row("bottom msg")
menu.show()
```
