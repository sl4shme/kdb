import string
from datetime import datetime
import random
import shutil
import os
import re
import subprocess
import tinydictdb
import configparser

# remove path => id ou name ? yes id


class Kdb:
    def __init__(self):
        self.initConfig()
        self.initDir()
        self.initDb()

    def initConfig(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'dbDir': '~/.kdb/',
                             'text_application': '$EDITOR',
                             'other_application': '$BROWSER',
                             'enable_git': True,
                             'git_webpage': False,
                             'git_other': False,
                             'compress_webpage': False,
                             'adblock_webpage': False,
                             'compress_folder': False}

        if not os.path.isdir('~/.kdb'):
            os.mkdir('~/.kdb')
            with open('~/.kdb/config') as f:
                config.write(f)
        else:
            config.read('~/.kdb/config')
        self.config = config['DEFAULT']

    def initDir(self):
        if not os.path.isdir(self.config.dbDir):
            os.mkdir(self.config.dbDir)
        for name in ["text", "web", "other"]:
            name = self.config.dbDir + "/" + name
            if not os.path.isdir(name):
                os.mkdir(name)

    def initDb(self):
        dbPath = self.config.dbDir + 'db.json'
        self.db = tinydictdb.TinyDicyDb(dbPath)

    def getType(self, path):
        if os.path.isfile(path):
            command = ["file", "-b", "--mime-type", path]
            result = subprocess.check_output(command).decode("utf-8")
            result = result.splitlines()[0]
        elif os.path.isdir(path):
            result = "dir"
        elif 
        return result

    def create(self, path, tags=[], name=""):
            entry['fileType'] = self.getType(path)
            entry['fileType'] = dir 

        entry['tags'] = tags
        entry['uuid'] = ''.join([random.choice(string.ascii_letters +
                                string.digits) for n in range(8)])
        self.a_date = self.m_date = self.c_date = str(datetime.now())
        if name:
            entry['name'] = name
        else:
            entry['name'] = path
        if 



        shutil.copy2(path, config.path)
        db.addEntry(name, "text", os.path.basename(path), tags)

    def delete(**toSearch):
        entries = db.findEntries(**toSearch)
        for entry in entries:
            os.remove(config.path + entry["path"])
        db.deleteEntries(entries)

    def get(**toSearch):
        return db.findEntries(**toSearch)


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
