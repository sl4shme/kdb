import json

# data = []

# with open('data.txt') as f:
#    for line in f:
#        jsonl = json.loads(line)
#        data.append(jsonl)
#       print(json.dumps(jsonl))

# print(json.dumps(data))

with open('db.json') as f:
    datas = json.load(f)

print(filter(lambda kres: kres['id'] == 1, datas))
