# Data-Type Hint
Python’s type hints provide you with optional static typing to leverage the best of both static and dynamic typing.  

The purpose of using type hint is to make code more robust, and most of the issues could be caught at compile time itself, thus improving the development efficiency.  

syntax for adding type-hint:
1. for a parameter or variable:
```python
parameter: type
```
2. for return type in function:
```python
-> type
```

Example:
```python
# notice the type-hint, here type of name is mentioned as `str` which is string, and for return type, it's `str`, again it's a string
def say_hi(name: str) -> str:
    return f'Hi {name}'

greeting = say_hi('John')
print(greeting)
```

Besides `str` we could also use built-in types like `int`, `float`, `bool`, `bytes`

# Important:
It’s important to note that the Python interpreter ignores type hints completely.  
If we pass a number to the say_hi() function, the program will run without any warning or error:  

```python
# accepts a string and returns a string
def say_hi(name: str) -> str:
    return f'Hi {name}'

greeting = say_hi(123) # passing an integer/number
print(greeting)
```
Outcome:  
```python
Hi 123
```

To check the syntax for type hints, you need to use a static type checker tool. For ex: `mypy`  

use it like this: 
- pip install mypy
- mypy app.py

```python
name: str = 'Hello'
result = name - 23 # this would fail obv. as we're operating on two different types, which interpreter wouldn't be able to do so,
name = 100 # this would still work, just mentioned above python interpreter ignores type-hint for the assignment part

```
# Adding type hints for multiple types

```python
def add(x, y):
    return x + y
```
The above `add` function can work with `int` as well as `float` types both.  
hence, instead of defining `add` two times one for each type, we could add type hints for multiple supporting types.  














**Reference:**  
1. https://www.pythontutorial.net/python-basics/python-type-hints/
