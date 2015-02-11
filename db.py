import json
import string
import random
from datetime import datetime


PATH = 'db.json'


class Db:
    def __init__(self):
        # Add lock
        # Create if not exist
        with open(PATH) as f:
            self.json = json.load(f)

    def writeDb(self):
        with open(PATH, 'w') as f:
            json.dump(self.json, f, indent=0)

    def addEntry(self, name, fileType, path, tags, encrypt=False):
        uuid = ''.join([random.choice(string.ascii_letters + string.digits)
                       for n in range(8)])
        entry = {"uuid": uuid,
                 "name": name,
                 "type": fileType,
                 "path": path,
                 "tags": tags,
                 "encrypt": encrypt,
                 "a_date": datetime.now(),
                 "m_date": datetime.now(),
                 "c_date": datetime.now()}
        self.json.append(entry)
        self.writeDb()

    def delEntry(self):
        pass

    def findEntry(self):
        pass
