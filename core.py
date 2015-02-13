import shutil
import os
# imports
import db
import env


def create(name, path, tags):
    shutil.copy2(path, env.path.strip("db.json"))
    db.addEntry(name, "text", os.path.basename(path), tags)


def delete(self):
     os.remove(path)


def search(self):
    pass


def grep(self):
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


def get(self):
    pass
