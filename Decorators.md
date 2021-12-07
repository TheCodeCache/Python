# Decorator

It is strongly advised to understand `higher-order` function in order to understand decorators in python.  
in fact, this is pre-requisite,  
and to do that, follow [this](https://github.com/TheCodeCache/Python/blob/master/First-Class%20Functions.md)  

When we decorate a component (be it a function, or a variable, or a class etc.),  
it essentially means that we're simply attaching extra behavior to the component.  

For ex (read the following):  
https://en.wikipedia.org/wiki/Decorator_pattern  

There is a thin line b/w annotation and decorator, to know more refer [this](https://stackoverflow.com/a/37317724/6842300)  

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


# Class Decorator


**Reference:**  
1. https://www.datacamp.com/community/tutorials/decorators-python
2. https://realpython.com/primer-on-python-decorators/
3. https://python-course.eu/advanced-python/decorators-decoration.php
