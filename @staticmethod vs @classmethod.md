# @staticmethod vs @classmethod

To decide whether to use `@staticmethod` or `@classmethod` we need to look inside the method.  
If the method accesses other variables/methods from the class then use `@classmethod`.  
On the other hand, if the method does not touches any other parts of the class then use `@staticmethod`.  

```python
class Apple:

    _counter = 0

    @staticmethod
    def about_apple():
        print('Apple is good for you.')

        # note you can still access other member of the class
        # but you have to use the class instance 
        # which is not very nice, because you have repeat yourself
        # 
        # For example:
        # @staticmethod
        #    print('Number of apples have been juiced: %s' % Apple._counter)
        #
        # @classmethod
        #    print('Number of apples have been juiced: %s' % cls._counter)
        #
        #    @classmethod is especially useful when you move your function to another class,
        #       you don't have to rename the referenced class 

    @classmethod
    def make_apple_juice(cls, number_of_apples):
        print('Making juice:')
        for i in range(number_of_apples):
            cls._juice_this(i)

    @classmethod
    def _juice_this(cls, apple):
        print('Juicing apple %d...' % apple)
        cls._counter += 1
```

**Reference:**  
1. https://stackoverflow.com/a/36798076/6842300

