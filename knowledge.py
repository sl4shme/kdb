import string
from datetime import datetime
import random


class Knowledge:
    def __init__(self, **kwargs):
        if kwargs['dict']:
            self.fromDict(kwargs['dict'])
        else:
            try:
                self.path = kwargs['path']
                self.tags = kwargs['tags']
                self.encrypt = kwargs['encrypt']
                self.fileType = self.getType()
                self.uuid = ''.join([random.choice(string.ascii_letters +
                                    string.digits) for n in range(8)])
                self.a_date = self.m_date = self.c_date = str(datetime.now())
                if ('name' in kwargs.keys) and (kwargs['name']):
                    self.name = kwargs['name']
                else:
                    self.name = self.path
            except:
                raise ValueError("Wrong data passed")

    def getType():
        return 'text'

    def toDict():
        pass

    def fromDict(self, dict):
        for key in dict.keys():
            setattr(self, key, dict[key])
