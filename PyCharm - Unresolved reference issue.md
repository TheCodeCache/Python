# Unresolved reference issue in `PyCharm` – 

![image](https://user-images.githubusercontent.com/26399543/153941222-287a54df-964d-4fee-a44a-4eb0b9a91a13.png)  

If we import `file1.py` in `sub_file.py`, or vice-versa or even in general scenario, if we encouter import related errors,  
or if `PyCharm` throws the following error:  

```python
Unresolved reference 'file1'
```

In project explorer (left panel),  
just identify the least common parent b/w these 2 files (`file1.py` and `sub_file.py`)  
and right click,  
look for `Mark Directory as` -> `Sources Root`  
select this `Sources Root` to add this folder to the PyCharm interpreter's classpath  

this way, `PyCharm` would be able to recognize all the files under the above identified parent folder  
and would be able to import them,  

That's how we could resolve this common import errors  

**Reference:**  
1. https://stackoverflow.com/questions/21236824/unresolved-reference-issue-in-pycharm
2. https://stackoverflow.com/a/65893035/6842300

