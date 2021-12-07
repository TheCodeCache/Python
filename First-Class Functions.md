# First-Class Functions:
`Functions in Python are first class citizens.`  
This implies that they support operations such as being, passed as an argument, returned from a function, modified, and assigned to a variable.  
This is a fundamental concept to understand before we delve into creating Python decorators.  

To know more about it, there is similar concepts in `Scala` as well.  
please refer [this](https://github.com/TheCodeCache/Scala/blob/master/First-Class%20Functions.md)  

# Assigning Functions to Variables
Code:  
```python
def plus_one(number):
    return number + 1
# assigning a function as if it's a normal value
add_one = plus_one
add_one(5)
```
Output:  
```python
6
```

# Defining Functions Inside other Functions
Code:  
```python
# outer function
def plus_one(number):
    # inner function, also called **Nested Function**. It's not possible in java, though it's possible in scala
    def add_one(number): 
        return number + 1
    # calling inner function as a normal function from within the scope of outer function
    result = add_one(number) 
    # returning the result
    return result 
plus_one(4)
```
Output:  
```python
5
```
# Passing Functions as Arguments to other Functions
Code:  
```python
# utility function, we can very much think of this function like a lambda
def plus_one(number):
    return number + 1

# function as an argument
def function_call(function):
    number_to_add = 5
    return function(number_to_add)

# passing function as a parameter, we could also do this using lambda concept (i.e. inline function literals)
function_call(plus_one)
```
Output:  
```python
6
```
# Functions Returning other Functions
Code:  
```python
# this function returns a another function
def hello_function():
    def say_hi():
        return "Hi"
    return say_hi
# assigning the outcome of `hello_function()` to this `hello` variable, so type of 'hello' would be a function as it holds a function
hello = hello_function()
hello()
```
Output:  
```python
'Hi'
```
# Nested Functions have access to the Enclosing Function's Variable Scope
Code:  
```python
def print_message(message):
    "Enclosong Function"
    def message_sender():
        "Nested Function"
        print(message)

    message_sender()

print_message("Some random message")
```
Output:  
```python
Some random message
```

**Note:**  
Any function that either accepts a function as an argument, or return a function as its outcome, is called `Higher-Order` Function.
This `higher-order` function is not possible in object-oriented language like java, if it is then it is no more an object-oriented.

**Reference:**  
1. https://www.datacamp.com/community/tutorials/decorators-python

