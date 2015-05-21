from datetime import datetime
import os
import re
import shutil
import subprocess
import tinydictdb
import configparser
import tempfile


def sanitize(toClean):
    toClean = str(toClean)
    toClean = toClean.lower()
    toClean = re.sub("[^a-z0-9.]", "_", toClean)
    toClean = re.sub("_+", "_", toClean)
    return toClean


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
        for name in ["text", "other"]:
            name = self.config['dbDir'] + "/" + name
            if not os.path.isdir(name):
                os.mkdir(name)
        # if git : add .gitignore and git init

    def __initDb(self):
        dbPath = self.config['dbDir'] + '/db.json'
        self.db = tinydictdb.TinyDictDb(path=dbPath)

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
        self.m_date = self.c_date = str(datetime.now())
        if name:
            entry['name'] = name
        else:
            entry['name'] = path

        if entry['fileType'].split('/')[0] == 'text':
            shutil.copy(path, '{}/text/{}'.format(self.config['dbDir'],
                                                  sanitize(entry['name'])))
        elif entry['fileType'] == 'web':
            dlDir = self.dumpWebPage(path)
            shutil.copytree(dlDir.name,
                            '{}/other/{}'.format(self.config['dbDir'],
                                                 sanitize(entry['name'])))
            dlDir.cleanup()
        elif entry['fileType'] == 'dir':
            shutil.copytree(path,
                            '{}/other/{}'.format(self.config['dbDir'],
                                                 sanitize(entry['name'])))
        else:
            shutil.copy(path, '{}/other/{}'.format(self.config['dbDir'],
                                                   sanitize(entry['name'])))

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
                fName = "{}/text/{}".format(self.config['dbDir'],
                                            sanitize(entry['name']))
                os.remove(fName)
            elif entry['fileType'] in ['web', 'dir']:
                fName = "{}/other/{}".format(self.config['dbDir'],
                                             sanitize(entry['name']))
                shutil.rmtree(fName)
            else:
                fName = "{}/other/{}".format(self.config['dbDir'],
                                             sanitize(entry['name']))
                os.remove(fName)
        self.db.deleteEntries(entries)

    def get(self, **toSearch):
        return self.db.findEntries(**toSearch)

    def grep(self, toGrep, large=False):
        command = ["grep", "-l", "-r", toGrep, self.config['dbDir'],
                   "--exclude=db.json", "--exclude=config"]
        if not large:
            command.append("--exclude-dir=other")
        # IF git add exclude git / gitignore
        output = subprocess.check_output(command).decode("utf-8")
        result = []
        for line in output.splitlines():
            fileName = line.replace(self.config['dbDir'], '')
            fileName = fileName.split("/")[2]
            result.append(self.get(name=(lambda x: True
                                         if fileName == sanitize(x)
                                         else False))[0])
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
