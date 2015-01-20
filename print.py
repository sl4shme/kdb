import json
import timeit


with open('db.json') as f:
    datas = json.load(f)

def uselambda (datalist):
    names = list(filter(lambda kres: "aa" in kres['name'], datalist))
    return(names)

def usefor(datalist):
    result=[]
    for i in datalist:
        if "aa" in i["name"]:
            result.append(i)
    return(result)

print(uselambda(datas))
print(usefor(datas))

    #ids = list(filter(lambda kres: kres['id'] < 5, datas))
    #print(ids)
    #print(len(ids))

