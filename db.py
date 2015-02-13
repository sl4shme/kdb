import json
import string
import random
from datetime import datetime
import env


def readDb():
    with open(env.path) as f:
        datas = json.load(f)
    return datas


def writeDb(newJson):
    with open(env.path, 'w') as f:
        json.dump(newJson, f, indent=0)


def addEntry(name, fileType, path, tags, encrypt=False):
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
    newJson = readDb()
    newJson.append(entry)
    writeDb(newJson)


def deleteEntries(entries):
    newJson = readDb()
    for entry in entries:
        newJson.remove(entry)
    writeDb(newJson)


def findEntries(name="", fileType="", tags=[]):
    result = readDb()
    if name:
        result = [item for item in result if name in item['name']]
    if fileType:
        result = [item for item in result if fileType in item['type']]
    if tags:
        result = [item for item in result if set(tags).issubset(
                  item['tags'])]
    return(result)
