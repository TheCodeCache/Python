`Lists` and `dictionaries` are the most widely used built-in data types in Python. This makes them also the best-known data types in Python  
However, when it comes to `tuples`, we usually tend to compare with `List` get a doubt when to use what? 

**Tuples and Lists: similarity**  
- They are both used to store collection of data  
- They are both heterogeneous data types means that you can store any kind of data type  
- They are both ordered means the order in which you put the items are kept.  
- They are both sequential data types so you can iterate over the items contained.  
- Items of both types can be accessed by an integer index operator, provided in square brackets, [index]  

The **key difference** between the tuples and lists is that while the `tuples are immutable objects the lists are mutable`.  

As lists are mutable, Python needs to allocate an extra memory block in case there is a need to extend the size of the list object after it is created.  
In contrary, as tuples are immutable and fixed size, Python allocates just the minimum memory block required for the data.  
As a result, tuples are more memory efficient than the lists.  

Code:  
```python
import sys
a_list = list()
a_tuple = tuple()
a_list = [1,2,3,4,5]
a_tuple = (1,2,3,4,5)
print(f'bytes for the list object: {sys.getsizeof(a_list)}')
print(f'bytes for the tuple object: {sys.getsizeof(a_tuple)}')
```
Outcome:  
```python
Output:
bytes for the list object: 120
bytes for the tuple object: 80
```

When it comes to the time efficiency, again Lists have a slight advantage over the Tuples especially when lookup to a value is considered.  
However, in terms of initialization, both seem to be comparable:  
For ex:

```python
# file_name: time_test.py

import sys, platform
import time
print(platform.python_version())
start_time = time.time()
b_list = list(range(10000000))
end_time = time.time()
print("Instantiation time for LIST:", end_time - start_time)
start_time = time.time()
b_tuple = tuple(range(10000000))
end_time = time.time()
print("Instantiation time for TUPLE:", end_time - start_time)
start_time = time.time()
for item in b_list:
  aa = b_list[8000000]

end_time = time.time()
print("Lookup time for LIST: ", end_time - start_time)
start_time = time.time()
for item in b_tuple:
  aa = b_tuple[8000000]

end_time = time.time()
print("Lookup time for TUPLE: ", end_time - start_time)
```
```python
C:\Users\manoranjan.kumar\Desktop>python time_test.py
3.9.6
Instantiation time for LIST: 0.22316551208496094
Instantiation time for TUPLE: 0.21480250358581543
Lookup time for LIST:  0.5550267696380615
Lookup time for TUPLE:  0.5991277694702148
```

**When to use What?**  
If you have data which is not meant to be changed in the first place, you should choose tuple data type over lists.  
But if you know that the data will grow and shrink during the runtime of the application, you need to go with the list data type.  

**Reference:**  
1. https://towardsdatascience.com/python-tuples-when-to-use-them-over-lists-75e443f9dcd7


