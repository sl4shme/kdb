import shutil
import os
# imports
import db
import env

# remove path => id ou name ?


def create(name, path, tags):
    shutil.copy2(path, env.path)
    db.addEntry(name, "text", os.path.basename(path), tags)


def delete(toSearch):
    entries = db.findEntries(toSearch)
    for entry in entries:
        os.remove(env.path + entry["path"])
    db.deleteEntries(entries)


def get(toSearch={}):
    return db.findEntries(toSearch)


def grep(self):
    # grep -l -r
    pass


def edit(self):
    pass


def git(self):
    pass


def exportBkup(self):
    pass


def importBkup(self):
    pass


def encrypt(self):
    pass


def decrypt(self):
    pass
