# Memory Management

Python uses `reference counting` for memory management.  
It means that objects created in Python have a reference count variable that keeps track of the number of references that point to the object.  
When this count reaches zero, the memory occupied by the object is released.  

**Reference:**  
1. https://github.com/python/cpython/blob/7d6ddb96b34b94c1cbdf95baa94492c48426404e/Objects/obmalloc.c
2. https://realpython.com/python-memory-management/
3. 
