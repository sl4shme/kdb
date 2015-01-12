**KDB**
===================

What is it ?
--------------
KDB (Knowledge DataBase) is a lightweight simple solution to store, retrieve and manage knowledge.   
If one day you said to yourself : "I need to write this command somewhere" or "This configuration file could be usefull someday".
Then KDB is for you. 

Commands :
--------------

### new
>kdb new [path of file] [-t tag1,tag2] [-n name]

**Ex :**  
create a new resource (will open an editor):
 - kdb new -n "New resource"

Import exising file (same result):
 - kdb new plop.py -n "python basics" -t python,dev
 - cat plop.py | kdb new -n "python basics" -t python,dev
 - kdb new -n "python basics" -t python,dev < plop.py

Import webpage:
 - kdb new https://www.python.org/dev/peps/pep-0008/ -t python -n "pep8"

Import image:
 - kdb new graph.jpeg -t graph,db

If no tags specified, user will be prompted.
If no name specified, default to filename.  

### search
>kdb search [-i id] [-t tag1,tag2] [-n name] [-r] [-c creation_date] [-m modification_date] [-a access_date]

**Ex :**  
List all resources tagged python:
 - kdb search -t python

List all resources with name containing python:
 - kdb search python
 - kdb search -r "/^python/"

List all resources created on 2014 :
 - kdb search -c \*\*/\*\*/2014

List all resources accessed less than 3 hours ago:
 - kdb search -a 3H  

### show
>kdb show [id] [-n name] [-t tag]

**Ex :**  
Show "python basics" resource:
 - kdb show -n "python basics"
 - kdb show 1  

 Binaries used to display resources are set in config file (default to cat/firefox/eog).  

### edit
>kdb edit [id] [-t tag1,tag2] [-n name]

**Ex :**  
Edit the "python basics" resource (works only on type=text):
 - kdb edit -n "python basics"
 - kdb edit 1

Edit the tags of "python basics" resource:
 - kdb edit -n "python basics" -t newtag1,newtag2

 Edit the name of "python basics" resource :
 - kdb edit 1 -n "python basics : conditionals"  

### rm 
>kdb rm [-i id] [-t tag1,tag2] [-n name]

**Ex :**  
Remove the resource with id 1:
 - kdb rm -i 1

Remove all resources tagged Python:
 - kdb rm -t python

Remove all resources piped from search command:
 - kdb search -a 3h | kdb rm  

### push
>kdb push

**Ex :**  
Push your database on the configured Git repo:
 - kdb push  

### pull
>kdb pull

**Ex :**   
Pull your database from the configured Git repo:
 - kdb pull   

### export
>kdb export filename.tar.gz

**Ex :**  
Export your database:
 - kdb export backup.tar.gz

Partial export:
 - kdb search -t python | kdb export python.tar.gz   

### import
>kdb import db.tar.gz

**Ex :**   
Import a database:
 - kdb import backup.tar.gz  


Architecture:
--------------

The db is stored in a directory:
<pre>
+-- _.kdb
|   +-- config
|   +-- db.json 
|   +-- 1_python_basics
|   +-- 2_sshd_config
|   +-- 3_shematics.jpeg
|   +-- 4_pep8
|       +-- index.html 
|       +-- style.css 
|       +-- script.js 
</pre>

Each resource is composed of:
 - A file (or a folder in the case of a webpage)
 - A JSON record in the db.json file in the form of:

> 
