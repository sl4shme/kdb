# Limitations : Works with Json types : int, float, list, dict, bool
#               There should be no type changes between the 2 data structure
#                     a: [1, 2] to a: {1: 2} will raise TypeError
#               Lists are treated as list if listAsSet is False:
#                     b: [1,2,3,4]  to [1,3,4] will report :
#                       -change 2 to 3
#                       -change 3 to 4
#                       -deleted 4
#               If listAsSet is set to True (default):
#                     b: [1,2,3,4]  to [1,3,4] will report :
#                       -deleted 2
#               If listAsSet is set to True:
#                     In a list of dictionnary, dictionnary's will be cheked
#                     for an 'id' key that identifies them:
#                     'id' can be modified by changing listDictIdentifier
#                     [{'id': 1, 'name': 'test'}] to [{'id': 1, 'name': 'try'}]
#                     will report:
#                           change test to try
#                     [{'name': 'test'}] to [{'name': 'try'}]
#                     will report:
#                           deleted {'name': 'test'}
#                           added {'name': 'try'}
#               If listAsSet is set to True:
#                   [1,1,1] will be treated as [1]
import json


class Comparator:
    def __init__(self, obj1=None, obj2=None, listAsSet=True,
                 listDictIdentifier='id'):
        self.listAsSet = listAsSet
        self.listDictIdentifier = listDictIdentifier
        self.v1 = obj1
        self.v2 = obj2
        self.loadFromJson('./vr1', './vr2')
        self.recap = []
        self.currPath = ['root']
        self.compare(self.v1, self.v2)

    def loadFromJson(self, path1, path2):
        with open(path1) as f:
            self.v1 = json.load(f)
        with open(path2) as f:
            self.v2 = json.load(f)

    def compare(self, v1, v2):
        if v1 == v2:
            pass  # No change in this couple
        elif v1 is None:
            path = []
            for i in self.currPath:
                path.append(i)
            change = {'in': path, 'type': 'add',
                      'old': None, 'new': v2}
            self.recap.append(change)
        elif v2 is None:
            path = []
            for i in self.currPath:
                path.append(i)
            change = {'in': path, 'type': 'del',
                      'old': v1, 'new': None}
            self.recap.append(change)
        else:
            if type(v1) == type(v2):
                if type(v1) in [bool, int, str, float]:
                    path = []
                    for i in self.currPath:
                        path.append(i)
                    change = {'in': path, 'type': 'chg',
                              'old': v1, 'new': v2}
                    self.recap.append(change)
                elif (type(v1) == list) and (self.listAsSet):
                    # self.currPath.append('list')
                    for cpl in self.couple(v1, v2):
                        self.currPath.append(cpl[1])
                        self.compare(cpl[0], cpl[1])

                        if len(self.currPath) != 1:
                            self.currPath.pop()
                elif (type(v1) == list) and (not self.listAsSet):
                    # self.currPath.append('list')
                    if len(v1) > len(v2):
                        lenght = len(v1)
                    else:
                        lenght = len(v2)
                    for i in range(0, lenght):
                        try:
                            a1 = v1[i]
                        except IndexError:
                            a1 = None
                        try:
                            a2 = v2[i]
                        except IndexError:
                            a2 = None
                        self.compare(a1, a2)
                    # if self.currPath != ['root']:
                        # self.currPath.pop()
                elif type(v1) == dict:
                    # self.currPath.append("dict")
                    keys1 = set(v1.keys())
                    keys2 = set(v2.keys())
                    keys = keys1.union(keys2)
                    for key in keys:
                        self.currPath.append(key)
                        self.compare(v1.get(key), v2.get(key))
                        if self.currPath != ['root']:
                            self.currPath.pop()
                    # if self.currPath != ['root']:
                        # self.currPath.pop()
                else:
                    raise TypeError("Unsupported type : val: {},"
                                    " type: {}".format(str(v1), str(type(v1))))
            else:
                path = []
                for i in self.currPath:
                    path.append(i)
                change = {'in': path, 'type': 'chg',
                          'old': v1, 'new': v2}
                self.recap.append(change)

    def couple(self, v1, v2):
        idf = self.listDictIdentifier
        oldWithIdf = []
        oldWithoutIdf = []
        for entry in v1:
            if (type(entry) == dict) and (idf in entry.keys()):
                oldWithIdf.append(entry)
            else:
                oldWithoutIdf.append(entry)

        newWithIdf = []
        newWithoutIdf = []
        for entry in v2:
            if (type(entry) == dict) and (idf in entry.keys()):
                newWithIdf.append(entry)
            else:
                newWithoutIdf.append(entry)

        oldValues = set([entry[idf] for entry in oldWithIdf])
        newValues = set([entry[idf] for entry in newWithIdf])
        added = newValues - oldValues
        removed = oldValues - newValues
        common = oldValues.intersection(newValues)
        result = []
        for a in added:
            result.append([None, [entry for entry in newWithIdf
                           if entry[idf] == a][0]])
        for r in removed:
            result.append([[entry for entry in oldWithIdf
                            if entry[idf] == r][0], None])
        for c in common:
            result.append([[entry for entry in oldWithIdf
                            if entry[idf] == c][0],
                          [entry for entry in newWithIdf
                           if entry[idf] == c][0]])

        for val in oldWithoutIdf:
            if val not in newWithoutIdf:
                result.append((val, None))
        for val in newWithoutIdf:
            if val not in oldWithoutIdf:
                result.append((None, val))

        return result
