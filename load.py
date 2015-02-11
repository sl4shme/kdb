import json
import random
import string

data = []
for num in range(1, 5):
    name = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    obj = {"id": num,
           "name": name,
           "type": "text",
           "path": "1_python_basics",
           "tags": ["python", "dev"],
           "encrypt": "false",
           "a_date": "2015-01-12 16:03:44",
           "m_date": "2015-01-12 16:03:44",
           "c_date": "2015-01-12 16:03:44"}
    data.append(obj)

with open('db.json', 'w') as f:
    json.dump(data, f, indent=0)

