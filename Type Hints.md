
# Data-Type Hint in Python
Python’s type hints provide you with optional static typing to leverage the best of both static and dynamic typing.  

The purpose of using type hint is to make code more robust, and most of the issues could be caught at compile time itself, thus improving the development efficiency.  

However, **Python `Interpreter` does `NOT` honor the type-hints** which is evident as follows:

```python
# declared ratings variable as `int` but was not honored by `Interperter`
>>> ratings: int = [1, 2, 3]
>>> ratings
[1, 2, 3]
>>> type(ratings)
<class 'list'>
>>>
```

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

# Using a static type checker tool: `mypy` 

Python doesn't have an official static type checker tool.  
At the moment, the most popular third-party tool is `Mypy`. Since `Mypy` is a third-party package,  
we need to install it like this:  
```
pip install mypy
```

we can check the type before running the program by using the following command:  
```
mypy app.py
```

It shows error in the following message/format:  
```
app.py:5: error: Argument 1 to "say_hi" has incompatible type "int"; expected "str"
Found 1 error in 1 file (checked 1 source file)
```
if we correct these issues, and re-run the above cmd, then it displays a success message:  
```
Success: no issues found in 1 source file
```

# Adding type hints for multiple types

```python
def add(x, y):
    return x + y
```
The above `add` function can work with `int` as well as `float` types both.  
hence, instead of defining `add` two times one for each type, we could add type hints for multiple supporting types.  

For Ex:
```python
# this is applicable to only for python 3.10 version or later
def add(x: int | float, y: int | float) -> int | float:
    return x + y
```

# Adding type hints for lists, dictionaries, and sets

```python
from typing import List

ratings: List[int] = [1, 2, 3]
```
# None type
If a function doesn’t explicitly returns a value, you can use None to type hint the return value.  
For Example:  
```python
def log(message: str) -> None:
    print(message)
```

**Re-iterating:**  
Python `Interpreter` always ignores the type-hints and checks for actual type at run time,  
type-hints are only meaningful when we want to kind of catch possible errors at compile time,  

**Reference:**  
1. https://www.pythontutorial.net/python-basics/python-type-hints/

