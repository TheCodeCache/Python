# Deeper undestanding of Python - 

To have a great internal knowledge of Python, these are the resources (source code files), we should explore.  
1. **`builtins.py`** - ths is just like java.lang.* in Java and scala.packages Predef in Scala  
  abs()  
  all()  
  any()  
  ascii()  
  bin()  
  breakpoint()  
  callable()  
  delattr()  
  dir()  
  exit()  
  format()  
  getattr()  
  globals()  
  locals()  
  hasattr()  
  hash()  
  help()  
  id()  
  input()  
  isinstance()  
  issubclass()  
  iter()  
  len()  
  compile()    
  exec()  
  eval()  
2. **`gc.py`**  
  enable() -- Enable automatic garbage collection.  
  disable() -- Disable automatic garbage collection.  
  isenabled() -- Returns true if automatic collection is enabled.  
  collect() -- Do a full collection right now.  
  get_count() -- Return the current collection counts.  
  get_stats() -- Return list of dictionaries containing per-generation stats.  
  set_debug() -- Set debugging flags.  
  get_debug() -- Get debugging flags.  
  set_threshold() -- Set the collection thresholds.  
  get_threshold() -- Return the current the collection thresholds.  
  get_objects() -- Return a list of all objects tracked by the collector.  
  is_tracked() -- Returns true if a given object is tracked.  
  is_finalized() -- Returns true if a given object has been already finalized.  
  get_referrers() -- Return the list of objects that refer to an object.  
  get_referents() -- Return the list of objects that an object refers to.  
  freeze() -- Freeze all tracked objects and ignore them for future collections.  
  unfreeze() -- Unfreeze all objects in the permanent generation.  
  get_freeze_count() -- Return the number of objects in the permanent generation.  

3. **`time.py`**

4. **`thread.py`**

5. **`multiprocessing package`**

6. **`_pickle.py`**

7. **`_socket.py`**

8. **`marshal.py`**

9. **`parser.py`**

10. **`sys.py`**

11. **`os.py`**


