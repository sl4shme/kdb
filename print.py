import json


with open('db.json') as f:
    datas = json.load(f)


def useitem():
    result2 = [item for item in datas if "aa" in item['name']]
    return(result2)

print("Item "+str(useitem()))
