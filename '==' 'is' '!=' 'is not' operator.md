# Equality Operator:

`==` and `!=` compare the value of two objects, whereas,  
`is` and `is not` operators compare whether two variables refer to the same object in memory  

Typically, is operator is faster than == because it checks the hashcode of the two objects, which is a kind of constant time operations.  
Here, with objects, we mean, whether two objects are identical, in the sense they both are pointing to the same address in memory.  

**Reference:**  
1. https://lerner.co.il/2015/06/16/why-you-should-almost-never-use-is-in-python/
2. https://realpython.com/python-is-identity-vs-equality/

