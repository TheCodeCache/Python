# Global Interpreter Lock i.e. `GIL` –

`It is a mutex (or a lock) that allows only one thread to hold the control of the Python interpreter.  
we need to lock the complete interpreter mainly because the underlying CPython's memory mgmt module is not thread-safe.`  
This means that only one thread can be in a state of execution at any point in time,  
It can be a performance bottleneck in CPU-bound and multi-threaded code.  

The `GIL` allows only one thread to execute at a time even in a multi-threaded architecture with more than one CPU core

**The Root Problem:** –  

This `reference count` variable needed protection from race conditions where two threads increase or decrease its value simultaneously.  
If this happens, it can cause either leaked memory that is never released or,  
even worse, incorrectly release the memory while a reference to that object still exists.  
This can cause crashes or other “weird” bugs in your Python programs.  

This `reference count` variable can be kept safe by adding locks to all data structures that are shared across threads  
so that they are not modified inconsistently.  
But adding a lock to each object or groups of objects means multiple locks will exist which can cause another problem—Deadlocks.  
Another side effect would be decreased performance caused by the repeated acquisition and release of locks.  

The `GIL` is a single lock on the interpreter itself which adds a rule that execution of any Python bytecode requires acquiring the interpreter lock.  
This prevents deadlocks (as there is only one lock) and doesn't introduce much performance overhead.  
But it effectively makes any CPU-bound Python program single-threaded.  



**Reference:**  
1. https://realpython.com/python-gil/


