**KDB**
===================

What is it ?
--------------


Commands :
--------------


**new**
-------
>new [path of file] [-t tag1,tag2] [-n name]

**Ex :**
create a new note (will open an editor):
 >kdb new -n "New note" 

Import exising file (same result):
 >kdb new plop.py -n "python basics" -t python,dev
 >OR
 >cat plop.py | kdb new -n "python basics" -t python,dev
 >OR
 >kdb new -n "python basics" -t python,dev < plop.py

Import webpage:
 >kdb new https://www.python.org/dev/peps/pep-0008/ -t python -n "pep8"
 
Import image:
>kdb new graph.jpeg -t graph,db

If no tags specified, user will be prompted.
If no name specified, default to filename.



**edit**
-------
>kdb edit [id] [-t tag1,tag2] [-n name]

**Ex :**
Edit the "python basics" note (works only on type=text):
 >kdb edit -n "python basics"
 >OR
 >kdb edit 1

Edit the tags of "python basics" note:
 >kdb edit -n "python basics" -t newtag1,newtag2
 
 Edit the name of "python basics" note :
 >kdb edit 1 -n "python basics : conditionals"
 


 **search**
-------
>search [-i id] [-t tag1,tag2] [-n name] [-r]

**Ex :**
List all ressources tagged python:
 > - kdb search -t python
 
 List all ressources with name containing python:
 > - kdb search python

-r = regex mode
