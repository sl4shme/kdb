**KDB**
===================

What is it ?
--------------


Commands :
--------------


### new
>new [path of file] [-t tag1,tag2] [-n name]

**Ex :**  
create a new note (will open an editor):
> - kdb new -n "New note"

Import exising file (same result):
> - kdb new plop.py -n "python basics" -t python,dev
> - cat plop.py | kdb new -n "python basics" -t python,dev
> - kdb new -n "python basics" -t python,dev < plop.py

Import webpage:
> - kdb new https://www.python.org/dev/peps/pep-0008/ -t python -n "pep8"

Import image:
> - kdb new graph.jpeg -t graph,db

If no tags specified, user will be prompted.
If no name specified, default to filename.



### edit
>kdb edit [id] [-t tag1,tag2] [-n name]

**Ex :**  
Edit the "python basics" note (works only on type=text):
> - kdb edit -n "python basics"
> - kdb edit 1

Edit the tags of "python basics" note:
> - kdb edit -n "python basics" -t newtag1,newtag2

 Edit the name of "python basics" note :
> - kdb edit 1 -n "python basics : conditionals"



### search
-------
>search [-i id] [-t tag1,tag2] [-n name] [-r] [-c creation_date] [-m modification_date] [-a access_date]

**Ex :**  
List all ressources tagged python:
> - kdb search -t python

List all ressources with name containing python:
> - kdb search python
> - kdb search -r "/^python/"

List all ressources created on 2014 :
> - kdb search -c \*\*/\*\*/2014

List all ressources accessed less than 3 hours ago:
> - kdb search -a 3H




