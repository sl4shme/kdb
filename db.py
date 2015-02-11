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
        timestamp = str(datetime.now())
        # datetime.strptime(sstr, "%Y-%m-%d %H:%M:%S.%f")
        entry = {"uuid": uuid,
                 "name": name,
                 "type": fileType,
                 "path": path,
                 "tags": tags,
                 "encrypt": encrypt,
                 "a_date": timestamp,
                 "m_date": timestamp,
                 "c_date": timestamp}
        self.json.append(entry)
        self.writeDb()

    def delEntry(self):
        pass

    def findEntry(self, name):
        result = [item for item in self.json if name in item['name']]
        return(result)
