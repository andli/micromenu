# micromenu

![CI and CD](https://github.com/andli/micromenu/workflows/CI%20and%20CD/badge.svg)

A minimalistic command line menu for Python, with a title and an optional message bar. Callable functions are attached to each menu item.

```terminal
╭─── test ───────────────────────────────────────────────╮
│ this is a message                                      │
╞════════════════════════════════════════════════════════╡
│ 1: item1                                               │
│ 2: item2                                               │
│ 0: Exit                                                │
╰────────────────────────────────────────────────────────╯
Action number:
```

## Installation

```bash
python3 -m pip install micromenu
```

## Example usage

```python
import micromenu

menu = micromenu.Menu("test", "this is a message")
menu.add_function_item("item1", lambda x: print(x), {'x':"testparam"})
menu.add_function_item("item2", lambda x: print(x), {'x':"testparam"}))
menu.show()
```
