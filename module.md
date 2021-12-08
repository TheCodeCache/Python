# A python `module`

A python `module` is not more than just a simple python file (*.py) containing python code  

For ex:
```python
# save this as hello_world.py file
def say():
  print('hello-world')
```

In the above code-snippet:  
as per the terminology in python, we call `hello_world` as `module`  

# `import` a module
now, there are ways to import this module, as follows:  
**note:** what we import is nothing but a full-fledged object, remember functions are also a first-class objects in python unlike in OOP languages (for ex: java)  
1. import hello_world
2. import hello_world as hello
3. from hello_world import say
4. from hello_world import say as say_hello
5. from hello_world import *

For the last point where we `import *` is not considered as good practice,  
as it could override the objects with the same name getting imported from a different modules.  
hence, we should always be very specific in terms of what we import to avoid any surprises (i.e. issues) during the course of s/w development.  

# how python `searches` for a module being imported:
Python will search for the module.py file from the following sources:  

1. The current folder from which the program executes.  
2. A list of folders specified in the PYTHONPATH environment variable, if we set it before.  
3. An installation-dependent list of folders that we configured when we install Python.  

Python stores the resulting search path in the `sys.path` variable that comes from the `sys` module.  
i.e.
```python
import sys

for path in sys.path: # notice sys.path is a `list`
    print(path)
```
Outcome:  
```python
C:\Program Files\Python39\python39.zip
C:\Program Files\Python39\DLLs
C:\Program Files\Python39\lib
C:\Program Files\Python39
C:\Users\manoranjan.kumar\AppData\Roaming\Python\Python39\site-packages
C:\Program Files\Python39\lib\site-packages
```

# IMPORTANT: 
# `modify` the Python `module search path at runtime`:
Python allows us to change the module search path (add, remove, update) at runtime by modifying the sys.path variable.  
This allows us to store module files in any folder of our choice.  
```python
import sys
sys.path.append('D:\\modules\\') # can use any standard `api` from `list` to update the `search-path`
```

**Reference:**  
1. https://www.pythontutorial.net/python-basics/python-module-search-path/

