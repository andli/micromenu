# micromenu

A minimalistic command line menu for Python, with a title and an optional message bar. Callable functions are attached to each menu item.

```terminal
╭─── test ───────────────────────────────────────────────╮
│ this is a message                                      │
╞════════════════════════════════════════════════════════╡
│ 1: title1                                              │
│ 0: Exit                                                │
╰────────────────────────────────────────────────────────╯
Action number:
```

## Example

```python
import micromenu

menu = micromenu.Menu("test", "this is a message")
menu.add_function_item("title1", lambda x: print(x), {'x':"testparam"})
menu.show()
```
