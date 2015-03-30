import shutil
import os
import subprocess
import tinydictdb
import configparser

# remove path => id ou name ? yes id


# Config file management
config = configparser.ConfigParser()
config['DEFAULT'] = {'dbDir': '~/.kdb/',
                     'text_application': '$EDITOR',
                     'other_application': '$BROWSER'}

if not os.path.isdir('~/.kdb'):
    os.mkdir('~/.kdb')
    with open('~/.kdb/config') as f:
        config.write(f)
else:
    config.read('~/.kdb/config')

config = config['DEFAULT']


# Kdb directory management
if not os.path.isdir(config.dbDir):
    os.mkdir(config.dbDir)
for name in ["text", "web", "other"]:
    name = config.dbDir + "/" + name
    if not os.path.isdir(name):
        os.mkdir(name)

dbDir = config.dbDir + 'db.json'
db = tinydictdb.TinyDicyDb(dbDir)


def create(name, path, tags):
    shutil.copy2(path, config.path)
    db.addEntry(name, "text", os.path.basename(path), tags)


def delete(**toSearch):
    entries = db.findEntries(**toSearch)
    for entry in entries:
        os.remove(config.path + entry["path"])
    db.deleteEntries(entries)


def get(**toSearch):
    return db.findEntries(**toSearch)


def getType(path):
    command = ["file", "-b", "--mime-type", path]
    result = subprocess.check_output(command).decode("utf-8")
    result = result.splitlines()[0]
    return result


def grep(toGrep):
    command = ["grep", "-l", "-r", toGrep, config.path, "--exclude=db.json"]
    output = subprocess.check_output(command).decode("utf-8")
    result = []
    for line in output.splitlines():
        pathName = os.path.basename(line)
        result.append(get(path=pathName)[0])
    return result


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


def downloadWebPage(self):  # add addblock option
    pass
