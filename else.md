# Usage of `else` block:

An `else` block can be used in multiple scenarios in python demonstrated below:

1. **try-else**

```python
try:
  # code
except:
  # code
else:
  # code
finally:
  # code
```
A minute difference b/w `else` and `finally` block is that, a `finally` block will always execute irrespective of what happens with try block,  
whereas `else` block will only be executed once try block worked normally without raising any issues/exceptions  
However, when `try` block does not emit any exception, in that case, first `else` block will execute followed by `finally` block  

2. **while-else**

```python
while(condition):
  # code
  # break statement
  # code
else:
  # code
```
When `break` encounters, it does not execute `else` block, otherwise,  
`else` will be invoked only when its condition was not met.  

3. **for-else**

```python
for item in list:
  # code
  # break statement
  # code
else:
  # code
```
with `for-else` scnenarios, `else` block gets executed when either there are no items in the iterables in the first place or it runs out of items while execution,  
however, whenever, `break` statement will encounter, `else` block will be ignored.  

4. **if-else**

```python
this is most typical cases that we're aware so, an example is not needed.  
If you're here that means you already know how to use `if-else` constructs in any language,  
```
