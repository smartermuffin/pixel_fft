import copy

class fileParams:
    def __init__(self):
        self.getCount = 0

        self.params = dict()
        self.params["update_delay"]=2
        self.params["onoff"]=1

    def _updateParams(self):
        for key in self.params:
            f  = open("/var/tmp/" + key)
            self.params[key] = int(f.read())
            f.read()
            f.seek(0)
        #print self.params


    def getParams(self):

        if self.getCount % 25 == 0:
            self._updateParams()

        p = copy.deepcopy(self.params)
        self.getCount +=1

        return p


