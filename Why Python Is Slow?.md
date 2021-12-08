# Why Python is Slow:



# How to make it Fast:
- Use `built-in C-modules` in Python like range()
- `I/O-tasks` release the GIL so they can be threaded; we can wait for many tasks to finish simultaneously
- Run CPU-tasks in parallel by `multiprocessing`
- Create and import our own `C-module` into Python; we extend Python with pieces of compiled C-code that are 100x faster than Python.
- Not an experienced C-programmer? Write Python-like code that `Cython` compiles to C and then neatly packages into a Python package.  
    It offers the readability and easy syntax of Python with the speed of C (more info)

"A must read:  
**Reference:**  
https://medium.com/geekculture/why-is-python-so-slow-and-how-to-speed-it-up-485b5a84154e

