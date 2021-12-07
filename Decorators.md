# Decorator

It is strongly advised to understand `higher-order` function in order to understand decorators in python.  
in fact, this is pre-requisite,  
and to do that, follow [this](https://github.com/TheCodeCache/Python/blob/master/First-Class%20Functions.md)  

When we decorate a component (be it a function, or a variable, or a class etc.),  
it essentially means that we're simply attaching extra behavior to the component.  

For ex (read the following):  
https://en.wikipedia.org/wiki/Decorator_pattern  

There is a thin line b/w annotation and decorator, to know more refer [this](https://stackoverflow.com/a/37317724/6842300)  
However, for the sake of terminology,  
we usually say: `annotate` a function/variable/class, similarly  
we could say: `decorate` a function/variable/class in python,  
though there is difference b/w the two, as `annotation` only deals with `metadata` aspect whereas the `decorator` helps to `enhances` the functionality.  

So, in Python, we've multiple types of decorators that applies to a:
1. Function
2. Class

# Function Decorator
Code:  
```python
def uppercase_decorator(function):
    def wrapper():
        func = function()
        make_uppercase = func.upper()
        return make_uppercase

    return wrapper
```
```python
def say_hi():
    return 'hello there'

decorate = uppercase_decorator(say_hi)
decorate()
```
Outcome:  
```python
'HELLO THERE'
```
If we notice in the above code-snippets, we're not doing anything extra-ordinary, if we know how a [higher-order](https://github.com/TheCodeCache/Python/blob/master/First-Class%20Functions.md) function works, it becomes way simple  

so, there's just another way to do the same, i mean instead of explicitly invoking uppercase_decorator(say_hi) like a normal function, this we could do using @decorator syntax like below:  

```python
@uppercase_decorator
def say_hi():
    return 'hello there'

say_hi()
```
Outcome:  
```python
'HELLO THERE'
```
It gives us exactly same output as the first version, right. so, just observe the difference, if we get it, we're done with the decorator concept.   

So, let us clarify this syntax once and for all:  
```python
@decorator
def function():
    return ''

function()
```
this last line `function()` literally translates to `outcome = decorator(function())`, where decorator is also a normal `higher-order` function  

**Applying Multiple Decorators to a Single Function:**  
We can use multiple decorators to a single function. However, the decorators will be applied in the order that we've called them  

Code:  
```python
def split_string(function):
    def wrapper():
        func = function()
        splitted_string = func.split()
        return splitted_string

    return wrapper
```
```python
@split_string
@uppercase_decorator
def say_hi():
    return 'hello there'
say_hi()
```
Outcome:  
```python
['HELLO', 'THERE']
```
In the above code-snippet, the last function call `say_hi()` is equivalent to `outcome = split_tring(uppercase_decorator(say_hi()))`

**Accepting Arguments in Decorator Functions:**  
Code:  
```python
def decorator_with_arguments(function):
    def wrapper_accepting_arguments(arg1, arg2):
        print("My arguments are: {0}, {1}".format(arg1,arg2))
        function(arg1, arg2)
    return wrapper_accepting_arguments


@decorator_with_arguments
def cities(city_one, city_two):
    print("Cities I love are {0} and {1}".format(city_one, city_two))

cities("Nairobi", "Accra")
```
Outcome:  
```python
My arguments are: Nairobi, Accra
Cities I love are Nairobi and Accra
```

**Defining General Purpose Decorators:**  
Code:  
```python
def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    def a_wrapper_accepting_arbitrary_arguments(*args,**kwargs):
        print('The positional arguments are', args)
        print('The keyword arguments are', kwargs)
        function_to_decorate(*args)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print("No arguments here.")

function_with_no_argument()
```
Outcome:  
```python
The positional arguments are ()
The keyword arguments are {}
No arguments here.
```
Using positional arguments:
```python
@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print(a, b, c)

function_with_arguments(1,2,3)
```python
The positional arguments are (1, 2, 3)
The keyword arguments are {}
1 2 3
```
Keyword arguments are passed using keywords
```python
@a_decorator_passing_arbitrary_arguments
def function_with_keyword_arguments():
    print("This has shown keyword arguments")

function_with_keyword_arguments(first_name="Derrick", last_name="Mwiti")
```
Outcome:  
```python
The positional arguments are ()
The keyword arguments are {'first_name': 'Derrick', 'last_name': 'Mwiti'}
This has shown keyword arguments
```

# Best Practice with Decorators: 
It is advisable and good practice to always use `functools.wraps` when defining decorators. It will help a lot during troubleshooting activity.  
for ex:  
```python
import functools

def uppercase_decorator(func):
    @functools.wraps(func)
    def wrapper():
        return func().upper()
    return wrapper
```
```python
@uppercase_decorator
def say_hi():
    "This will say hi"
    return 'hello there'

say_hi()
```
Outcome:  
```python
'HELLO THERE'
```
Using this `functools`, we can now check the function's metadata, for ex:  
```python
say_hi.__name__
```
```python
'say_hi'
```
```python
say_hi.__doc__
```
```python
'This will say hi'
```


**Python Decorators Summary:**  

Decorators dynamically alter the functionality of a function, method, or class without having to directly use subclasses or change the source code of the function being decorated.  
It has several usecases:  
1. Authorization in Python frameworks such as Flask and Django
2. Logging
3. Measuring execution time
4. Synchromization

# Class Decorator
This kind of decorator is usually achieved by making its instances `callable` through `__call__` dunder method:  
It has been well explained [here](https://www.pythontutorial.net/advanced-python/python-class-decorators/)  

However, as for the best practice, we should generally use function based decorators, as it gives more flexibility than the class level decorators.

**Reference:**  
1. https://www.datacamp.com/community/tutorials/decorators-python
2. https://realpython.com/primer-on-python-decorators/
3. https://python-course.eu/advanced-python/decorators-decoration.php
4. https://wiki.python.org/moin/PythonDecoratorLibrary



