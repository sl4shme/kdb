import string
from datetime import datetime
import random
import shutil
import os
import re
import subprocess
import tinydictdb
import configparser
import tempfile


class Kdb:
    def __init__(self):
        self.__initConfig()
        self.__initDir()
        self.__initDb()

    def __initConfig(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'dbDir': '~/.kdb/',
                             '_text_application': '$EDITOR',
                             '_other_application': '$BROWSER',
                             '_enable_git': True,
                             '_git_webpage': False,
                             '_git_other': False,
                             '_compress_webpage': False,
                             '_adblock_webpage': False,
                             '_compress_folder': False,
                             'user_agent': '"User-Agent: Mozilla/5.0 (Windows;'
                                           ' U; Windows NT 5.1; en-US;'
                                           ' rv:1.9.2.12) Gecko/20101026'
                                           ' Firefox/3.6.12"'}

        homePath = os.path.expanduser('~/.kdb')
        cfgPath = homePath + '/config'
        if not os.path.isdir(homePath):
            os.mkdir(homePath)
        try:
            with open(cfgPath) as f:
                config.read(cfgPath)
        except FileNotFoundError:
            with open(cfgPath, 'w') as f:
                config.write(f)
        self.config = config['DEFAULT']

    def __initDir(self):
        self.config['dbDir'] = os.path.normpath(os.path.expanduser(
                                                self.config['dbDir']))
        if not os.path.isdir(self.config['dbDir']):
            os.mkdir(self.config['dbDir'])
        for name in ["text", "web", "other"]:
            name = self.config['dbDir'] + "/" + name
            if not os.path.isdir(name):
                os.mkdir(name)
        # if git : add .gitignore and git init

    def __initDb(self):
        dbPath = self.config['dbDir'] + '/db.json'
        self.db = tinydictdb.TinyDictDb(dbPath)

    def __getType(self, path):
        if os.path.isfile(path):
            command = ["file", "-b", "--mime-type", path]
            result = subprocess.check_output(command).decode("utf-8")
            result = result.splitlines()[0]
        elif os.path.isdir(path):
            result = "dir"
        elif re.search('.*https?://.*', path):
            result = "web"
        else:
            raise ValueError("The path provided is invalid.")
        return result

    def create(self, path, tags=[], name=""):
        entry = {}
        entry['fileType'] = self.__getType(path)
        entry['tags'] = tags
        entry['uuid'] = ''.join([random.choice(string.ascii_letters +
                                string.digits) for n in range(8)])
        self.a_date = self.m_date = self.c_date = str(datetime.now())
        if name:
            entry['name'] = name
        else:
            entry['name'] = path

        if entry['fileType'].split('/')[0] == 'text':
            shutil.copy(path, self.config['dbDir'] + '/text/' + entry['uuid'])
        elif entry['fileType'] == 'web':
            dlDir = self.dumpWebPage(path)
            shutil.copytree(dlDir.name,
                            self.config['dbDir'] + '/web/' + entry['uuid'])
# IF only one file : need to repasser dans le file type
            dlDir.cleanup()
        elif entry['fileType'] == 'dir':
            shutil.copytree(path,
                            self.config['dbDir'] + '/other/' + entry['uuid'])
        else:
            shutil.copy(path, self.config['dbDir'] + '/other/' + entry['uuid'])

        self.db.addEntries(entry)

    def dumpWebPage(self, url):
            td = tempfile.TemporaryDirectory()
            command = ["wget", "-E", "-H", "-k", "-K", "-p",
                       "--user-agent={}".format(self.config['user_agent']),
                       "--no-directories", "-P", td.name, url]
            code = subprocess.call(command, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
            if (code != 0) or (len(os.listdir(td.name)) == 0):
                raise ValueError("Error while trying to"
                                 " download {}".format(url))
            return td

    def delete(self, **toSearch):
        entries = self.db.findEntries(**toSearch)
        for entry in entries:
            if entry['fileType'].split('/')[0] == 'text':
                fName = self.config['dbDir'] + "/text/" + entry['uuid']
                os.remove(fName)
            elif entry['fileType'] == 'web':
                fName = self.config['dbDir'] + "/web/" + entry['uuid']
                shutil.rmtree(fName)
            elif entry['fileType'] == 'dir':
                fName = self.config['dbDir'] + "/other/" + entry['uuid']
                shutil.rmtree(fName)
            else:
                fName = self.config['dbDir'] + "/other/" + entry['uuid']
                os.remove(fName)
        self.db.deleteEntries(entries)

    def get(self, **toSearch):
        return self.db.findEntries(**toSearch)

    def grep(self, toGrep, large=False):
        command = ["grep", "-l", "-r", toGrep, self.config['dbDir'],
                   "--exclude=db.json", "--exclude=config"]
        if not large:
            command.append("--exclude-dir=web")
            command.append("--exclude-dir=other")
        # IF git add exclude git / gitignore
        output = subprocess.check_output(command).decode("utf-8")
        result = []
        for line in output.splitlines():
            uuid = line.replace(self.config['dbDir'], '')
            uuid = uuid.split("/")[2]
            result.append(self.get(uuid=uuid)[0])
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
