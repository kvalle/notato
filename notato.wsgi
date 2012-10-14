import sys 
import site 
import os.path
	
ALLDIRS = ['/home/kjetil/pyenvs/notes/lib/python2.7/site-packages']

# Remember original sys.path.
prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
new_sys_path = [] 
for item in list(sys.path): 
    if item not in prev_sys_path: 
        new_sys_path.append(item)
        sys.path.remove(item) 
sys.path[:0] = new_sys_path 

# Actually boot up application
notato_path = os.path.dirname(__file__)
sys.path.insert(0, notato_path)
from notato import app as application
