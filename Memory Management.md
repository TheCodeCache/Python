# Memory Management

Python uses `reference counting` for memory management.  
It means that objects created in Python have a reference count variable that keeps track of the number of references that point to the object.  
When this count reaches zero, the memory occupied by the object is released.  

