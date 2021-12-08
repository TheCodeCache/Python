# `timeit` module

we can run any random python code using timeit.Timer and check for their execution time,  

For ex:  

```python
import timeit

statements=["""\
try:
    b = 10/a
except ZeroDivisionError:
    pass""",
"""\
if a:
    b = 10/a""",
"b = 10/a"]

for a in (1,0):
    for s in statements:
        t = timeit.Timer(stmt=s, setup='a={}'.format(a))
        print("a = {}\n{}".format(a,s))
        print("%.2f usec/pass\n" % (1000000 * t.timeit(number=100000)/100000))
```
```python
a = 1
try:
    b = 10/a
except ZeroDivisionError:
    pass
0.08 usec/pass

a = 1
if a:
    b = 10/a
0.07 usec/pass

a = 1
b = 10/a
0.04 usec/pass

a = 0
try:
    b = 10/a
except ZeroDivisionError:
    pass
0.19 usec/pass

a = 0
if a:
    b = 10/a
0.01 usec/pass

a = 0
b = 10/a
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
  File "C:\Program Files\Python39\lib\timeit.py", line 177, in timeit
    timing = self.inner(it, self.timer)
  File "<timeit-src>", line 6, in inner
ZeroDivisionError: division by zero
>>>
```

**Reference:**  
1. https://stackoverflow.com/a/2522013/6842300

